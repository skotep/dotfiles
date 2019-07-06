"""Wrapper around common git methods"""

import click
import getpass
import subprocess as sp
import os
import re
import tempfile
import random
import shlex
import string
import time
from functools import update_wrapper
from itertools import groupby
from typing import Callable
from typing import Optional
from typing import Union
from typing import List
from typing import BinaryIO
import github
from github import Github
from github import Organization
from github import Repository
from github import PullRequest
from urllib.parse import urlparse

STAGED_MESSAGE = 'Stash staged files.'
UNTRACKED_MESSAGE = 'Stash untracked files.'

def randomWord(length):
    wordFile = open('/usr/share/dict/words')
    fileLength = os.stat('/usr/share/dict/words').st_size
    bufferLength = 2048
    result = ''
    while not result:
        offset = random.randint(0, fileLength // bufferLength) * bufferLength
        wordFile.seek(offset)
        segment = wordFile.read(bufferLength)
        words = [x for x in segment.split('\n')[1:-1] if len(x) == length and not x[0].istitle()]
        if words:
            result = words[random.randint(0, len(words) - 1)]
    return result

class NamedVar(object):
    def __init__(self, name: str, value: str, shellDesc: str):
        self.name = name
        self.value = value
        self.shellDesc = shellDesc

def varName(arg: Union[str, NamedVar]):
    if type(arg) is str:
        return arg
    else:
        return "${%s}" % arg.name

def varValue(arg: Union[str, NamedVar]):
    if type(arg) is str:
        return arg
    else:
        return arg.value

def splitIfNotEmpty(value):
  if not value:
      return []
  else:
      return value.split('\n')

def varGen(arg: NamedVar):
    return "%s=`%s`" % (arg.name, arg.shellDesc)

def varGens(args: List[Union[str, NamedVar]]):
    namedVars = [varGen(arg) for arg in args if type(arg) == NamedVar]
    return " \\\n".join(namedVars)

def varNames(args: List[Union[str, NamedVar]]):
    return [varName(arg) for arg in args]

def varValues(args: List[Union[str, NamedVar]]):
    return [varValue(arg) for arg in args]

def commandParent(args: List[str]):
    """Tell the parent or user to issue a necessary shell command."""
    COMMAND='Run this command: '
    click.echo(COMMAND + ' '.join([shlex.quote(arg) for arg in args]))

def rootRunnable(callFnIn):
    """Decorator providing option to run git command from git root."""
    def callFnOut(*args, **kwargs):
        if kwargs.pop('fromRoot', False):
            git = args[0]
            gitRoot = git.callAndGetUtf8(['rev-parse', '--show-toplevel'])
            args[1].insert(0, '-C')
            args[1].insert(1, gitRoot)
        return callFnIn(*args, **kwargs)
    return callFnOut

class GitWrapper(object):
    def __init__(self, verbose: bool):
        self.verbose = verbose

    @rootRunnable
    def call(self, args: List[Union[str, NamedVar]], exceptOnError: bool=True) -> None:
        """Call a git command and wait for it to complete."""
        argValues = varValues(args)
        command = 'git ' + ' '.join(argValues)
        if self.verbose:
            envVars = varGens(args)
            if envVars:
                envVars += '; '
            displayCommand = '(%sgit %s)' % (envVars, ' '.join(varNames(args)))
            click.echo(displayCommand)
        returncode = sp.Popen(['git'] + argValues, shell=False).wait()
        if returncode != 0 and exceptOnError:
            raise click.ClickException("%s failed with error %d" % (command, returncode))

    @rootRunnable
    def callAndPipe(self, args: List[Union[str, NamedVar]], shellDesc: str, callbackFunc: Optional[Callable[[bytes], None]], stdout: BinaryIO=sp.PIPE) -> None:
        """Call a git command, pipe the stdout, and pass it to a callback."""
        argValues = varValues(args)
        command = 'git ' + ' '.join(argValues)
        if self.verbose:
            envVars = varGens(args)
            if envVars:
                envVars += '; '
            displayCommand = '(%sgit %s)' % (envVars, ' '.join(varNames(args)))
            click.echo(displayCommand)
        p = sp.Popen(['git'] + argValues, shell=False, stdout=stdout)
        output, err = p.communicate()
        if p.returncode != 0:
            raise click.ClickException("%s failed with error %d" % (command, p.returncode))
        if callbackFunc:
            callbackFunc(output)

    @rootRunnable
    def callAndGetUtf8Var(self, args: List[Union[str, NamedVar]], varName: str) -> NamedVar:
        """Call a git command, pipe the stdout, and return it."""
        argValues = varValues(args)
        command = 'git ' + ' '.join(argValues)
        p = sp.Popen(['git'] + argValues, shell=False, stdout=sp.PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            raise click.ClickException("%s failed with error %d" % (command, p.returncode))
        shellDesc = 'git %s' % ' '.join(varNames(args))
        return NamedVar(varName, output.decode('utf-8').rstrip(), shellDesc)

    @rootRunnable
    def callAndGetUtf8(self, args: List[Union[str, NamedVar]], stdin: Optional[bytes]=None) -> str:
        """Call a git command, pipe the stdout, and return the shell result as UTF-8."""
        argValues = varValues(args)
        command = 'git ' + ' '.join(argValues)
        p = sp.Popen(['git'] + argValues, shell=False, stdout=sp.PIPE, stdin=sp.PIPE)
        output, err = p.communicate(input=stdin)
        if p.returncode != 0:
            raise click.ClickException("%s failed with error %d" % (command, p.returncode))
        return output.decode('utf-8').rstrip()

    @rootRunnable
    def callAndGetStatus(self, args: List[Union[str, NamedVar]]) -> bool:
        """Call a git command, pipe the stdout, and return True if successful."""
        argValues = varValues(args)
        command = 'git ' + ' '.join(argValues)
        returncode = sp.Popen(
                ['git'] + argValues, shell=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL).wait()
        return returncode == 0

passGitWrapper = click.make_pass_decorator(GitWrapper)

def mergeWithFixes(pullRequest: PullRequest.PullRequest, commit_title: str,
        commit_message: str, merge_method: str, sha: str):
    """Fixed version of PyGithub merge with commit_title, merge_method, and sha."""
    post_parameters = dict()
    post_parameters["commit_title"] = commit_title
    post_parameters["commit_message"] = commit_message
    post_parameters["merge_method"] = merge_method
    post_parameters["sha"] = sha
    headers, data = pullRequest._requester.requestJsonAndCheck(
	"PUT",
	pullRequest.url + "/merge",
	input=post_parameters
    )
    return github.PullRequestMergeStatus.PullRequestMergeStatus(pullRequest._requester, headers, data, completed=True)

def notOnMaster(f):
    """Decorator that creates a new branch when a command is run from master."""
    @passGitWrapper
    @click.pass_context
    def wrappedFunc(ctx, git, *args, **kwargs):
        currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])
        if currentBranch == 'master':
            # If master, create new branch and move files.
            ctx.invoke(new, move=True)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(wrappedFunc, f)


def requestReview(pullRequest: PullRequest.PullRequest, reviewers: List[str]):
    """Request review for a pull request."""
    post_parameters = dict()
    post_parameters["reviewers"] = reviewers
    headers, data = pullRequest._requester.requestJsonAndCheck(
	"POST",
	pullRequest.url + "/requested_reviewers",
	input=post_parameters,
        headers={'Accept': 'application/vnd.github.black-cat-preview+json'}
    )

def removeRevPrefix(text):
    """Remove rXX prefix from commit string."""
    return re.sub(r'^r\d+: ', '', text)

def pushState(git: GitWrapper):
    """Save current state by committing index and untracked files."""
    stagedFiles = git.callAndGetUtf8(['diff', '--name-only', '--cached'])
    if stagedFiles:
        # Commit staged files.
        git.call(['commit', '--quiet', '-m', STAGED_MESSAGE])

    untrackedFiles = git.callAndGetUtf8(['ls-files', '--modified', '--others', '--exclude-standard'], fromRoot=True)
    if untrackedFiles:
        # Commit untracked files
        git.call(['add', '--', '.'], fromRoot=True)
        git.call(['commit', '--quiet', '-m', UNTRACKED_MESSAGE])

def popState(git: GitWrapper):
    # Recover files and index stashed in the branch.
    if git.callAndGetUtf8(['show', '-s', '--format=%s', 'HEAD']) == UNTRACKED_MESSAGE:
        git.call(['reset', '--quiet', '--soft', 'HEAD~1'])
        git.call(['reset', '--quiet'])
    if git.callAndGetUtf8(['show', '-s', '--format=%s', 'HEAD']) == STAGED_MESSAGE:
        git.call(['reset', '--quiet', '--soft', 'HEAD~1'])


def getGithubRepo(git: GitWrapper) -> Repository.Repository:
    """Read git credentials and return github Repo object."""
    remote = git.callAndGetUtf8(['remote', 'get-url', 'origin'])

    url = urlparse(remote)
    fillInput = (
        'protocol=%s\n' % url.scheme +
        'host=%s\n' % url.netloc +
        'path=%s\n' % url.path +
        '\n'
    ).encode('utf-8')
            
    fillOutput = git.callAndGetUtf8(['credential', 'fill'], stdin=fillInput)
    creds = dict(re.findall(r'(\S+)=(\S+)', fillOutput))

    github = Github(creds.get('username'), creds.get('password'))

    orgName, repoName = url.path.strip('/').rstrip('.git').split('/', 1)
    org = github.get_organization(orgName)
    return org.get_repo(repoName)

@click.group(add_help_option=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True, help='Verbose output, echo git commands')
def cli(ctx, verbose):
    """Command-line tool for the 8th Wall source repository."""

    ctx.obj = GitWrapper(verbose=verbose)
    pass

@cli.command()
@click.pass_context
@click.argument('command', default=None, required=False)
def help(ctx, command):
    """Show help message for a command."""
    if command is None:
        click.echo(ctx.get_help())
    else:
        ctx.info_name = command
        click.echo(cli.commands[command].get_help(ctx))

def deleteFeature(git: GitWrapper, change: str):
    """Delete the local branch, remote branch, and pull requests."""
    # TODO(mc) For diffbase, make this the parent branch, not just master.
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])

    # Switch to master if we are deleting the active branch.
    if currentBranch == change:
        git.call(['checkout', 'master', '--quiet'])

    # Delete the local branch.
    git.call(['branch', '-D', change])

    # Get current user.
    user = getpass.getuser()

    # Get remote branch name.
    remoteBranch = '%s.%s' % (user, change)

    # Get remote branch URL.
    remoteUrl = git.callAndGetUtf8Var(["remote", "get-url", "origin"], "REMOTE")

    # Check if branch exists on remote
    branchOnRemote = git.callAndGetStatus(
            ["ls-remote", "--quiet", "--exit-code", "--heads", remoteUrl, remoteBranch])

    if branchOnRemote:
        # Delete remote branch.
        git.call(['push', 'origin', '--delete', '%s' % remoteBranch])


@cli.command()
@click.pass_context
@click.option('-m', '--move', is_flag=True, help='Move modified files into the change')
def new(ctx, move):
    """Create a new change and switch to it."""
    name = randomWord(5)
    ctx.invoke(change, force=True, move=move, delete=False, change=name)

@cli.command()
@passGitWrapper
@click.pass_context
def deleteme(ctx, git):
    """Delete the current change."""
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])
    ctx.invoke(change, force=False, move=False, delete=True, change=currentBranch)

@cli.command()
@passGitWrapper
@click.pass_context
@click.option('-f', '--force', is_flag=True, help='Create change if it does not exist')
@click.option('-m', '--move', is_flag=True, help='Move modified files into the change')
@click.option('-d', '--delete',  is_flag=True, help='Delete change')
@click.argument('change')
def change(ctx, git, force, move, delete, change):
    """Switch to a new change."""

    # Ensure master is clean. 
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])
    if change == 'master' and move:
        raise click.ClickException("Cannot move changes into master")

    if currentBranch == 'master' and not move:
        stagedFiles = git.callAndGetUtf8(['diff', '--name-only', '--cached'])
        untrackedFiles = git.callAndGetUtf8(['ls-files', '--modified', '--others', '--exclude-standard'], fromRoot=True)
        if stagedFiles or untrackedFiles:
            raise click.ClickException("master has modifications, move files with the change using '-m'.")

    if not force:
        try:
            # Verify that the branch exists.
            git.callAndGetUtf8(['rev-parse', '-q', '--verify', change])
        except click.ClickException:
            raise click.ClickException('Change \'%s\' does not exist' % change)

    # TODO(mc) Change to the code8 directory when switching between changes.
    # This has to be done with a shell wrapper function as a python script can't
    # change the parent shell that called it.
    # topLevel = git.callAndGetUtf8(['rev-parse', '-q', '--show-toplevel'])

    currentDir = os.getcwd()
    rootDir = git.callAndGetUtf8(['rev-parse', '--show-toplevel'])

    # Move to the root directory.
    os.chdir(rootDir)

    if not move:
        pushState(git)

    try:
        if delete:
            if change == 'master':
                raise click.ClickException("master cannot be deleted.")
            if click.confirm('Delete change %s?' % change, abort=True):
                deleteFeature(git, change)
                return
        if force and not git.callAndGetStatus(['show-ref', '--quiet', 'refs/heads/%s' % change]):
            try:
                # TODO(mc): Change this support branching not only from master.
                if currentBranch != 'master':
                    git.call(['checkout', 'master', '--quiet'])
                git.call(['checkout', '--quiet', '-b', change])
                ctx.invoke(status)
                click.echo('Switched to a new branch \'%s\'' % change);
            finally:
                # Recover files and index stashed in the branch.
                popState(git)
        else:
            try:
                # Checkout the new branch.
                git.call(['checkout', '--quiet', change])
                ctx.invoke(status)
                click.echo('Switched to branch \'%s\'' % change);
            finally:
                # Recover files and index stashed in the branch.
                popState(git)
    finally:
        # Check whether directory still exists.
        if not os.path.isdir(currentDir):
            # Tell the parent shell to cd to the root directory.
            commandParent(['cd', rootDir])

@cli.command()
@passGitWrapper
def status(git):
    """Show all unsubmitted changes to the change."""
    # Find the fork point for this branch.
    # TODO(mc): Change this to pass in the mainline branch that we started this change from,
    # currently it is hardcoded as master.
    forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')

    RED = '\033[31m'
    GREEN = '\033[32m'
    NOCOLOR = '\033[0m'

    shellDesc = 'xargs -I{} echo "%s{}"'
    def colorStatus(color):
        def func(stdout: bytes):
            output = stdout.decode('utf-8').rstrip()
            if output:
                lines = output.replace('\t', ' ').split('\n')
                click.echo('\n'.join([' ' + color + x[0] + NOCOLOR + ' ' + x[1:] for x in lines]))
        return func

    # Output tracked and committed files between staging and master.
    git.callAndPipe(['diff', forkPoint, '--cached', '--name-status'], shellDesc, colorStatus(GREEN))

    # Output files that are modified in the working directory.
    git.callAndPipe(['diff', '--name-status'], shellDesc, colorStatus(RED))

    untrackedPrefix = ' %s?%s  ' % (RED, NOCOLOR)
    shellDesc = 'xargs -I{} echo "%s{}"' % untrackedPrefix
    def listUntracked(stdout: bytes):
        output = stdout.decode('utf-8').rstrip()
        if output:
            lines = output.split('\n')
            click.echo('\n'.join([untrackedPrefix + x for x in lines]))
    # Output new files.
    git.callAndPipe(['ls-files', '--others', '--exclude-standard'], shellDesc,
            listUntracked, fromRoot=True)

def interactiveFileList(git, message):
    """List all modified, deleted, added or untracked files, and allow customization."""
    # Find the fork point for this branch.
    # TODO(mc): Change this to pass in the mainline branch that we started this change from,
    # currently it is hardcoded as master.
    forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')

    updatedFiles = set(splitIfNotEmpty(git.callAndGetUtf8(['diff', forkPoint, '--cached', '--name-only'])))
    newFiles = set(splitIfNotEmpty(git.callAndGetUtf8(['ls-files', '--modified', '--others', '--exclude-standard'], fromRoot=True)))
    allFiles = sorted(list(set(list(updatedFiles) + list(newFiles))))

    indexFile = tempfile.NamedTemporaryFile()

    with open(indexFile.name, "wb") as f:
        f.write(('# %s\n' % message).encode('utf-8'))
        f.write('\n'.join(allFiles).encode('utf-8'))

    EDITOR=os.environ.get('EDITOR', 'vi')
    returncode = sp.Popen([EDITOR, indexFile.name], shell=False).wait()
    if returncode != 0:
        raise click.ClickException("File edit failed with error %d" % (p.returncode))

    userFiles = set()
    with open(indexFile.name, "rb") as f:
        for line in f.readlines():
            strippedLine = line.decode('utf-8').strip()
            if strippedLine.startswith('#'):
                continue
            userFiles.add(strippedLine)

    addFiles = []
    deleteFiles = []

    for oneFile in updatedFiles:
        if not oneFile in userFiles:
            deleteFiles.append(oneFile)

    for oneFile in newFiles:
        if oneFile in userFiles:
            addFiles.append(oneFile)

    return (addFiles, deleteFiles)

@cli.command()
@passGitWrapper
def sync(git):
    """Sync latest updates from server and rebase."""

    # Get the current branch.
    currentBranch = git.callAndGetUtf8Var(['symbolic-ref', '--short', 'HEAD'], 'CURRENT')

    currentBranchIsMaster = (currentBranch.value == 'master')

    currentDir = os.getcwd()
    rootDir = git.callAndGetUtf8(['rev-parse', '--show-toplevel'])
    needsDirChange = False

    if not currentBranchIsMaster:
        # Switch to root dir.
        os.chdir(rootDir)
        # Save state in the current branch.
        pushState(git)
        # Switch to the master branch.
        git.call(['checkout', 'master'])

    # Sync remote state.
    git.call(['fetch'])

    masterAdvanced = False

    try:
        # Move the master branch forward. This must be a fast-forward as we
        # shouldn't be committing to master.
        # TODO(mc): Should this be a rebase if the current branch is master?
        git.call(['merge', '--ff-only'])
        masterAdvanced = True
    finally:
        if not currentBranchIsMaster:
            # Check whether directory to return to exists.
            needsDirChange = not os.path.isdir(currentDir)

            # Switch back to the topic branch.
            git.call(['checkout', currentBranch])

    try:
        if (not currentBranchIsMaster) and masterAdvanced:
            # Rebase off master.
            # TODO(mc): Change this behavior to support diffbase.
            git.call(['rebase', '--quiet', '--onto', 'master', 'master', currentBranch])
    finally:
        if not currentBranchIsMaster:
            # Recover state.
            popState(git)
            # Switch back to working dir.
            os.chdir(currentDir)
            if needsDirChange:
                # Tell the parent shell to cd to the working dir.
                commandParent(['cd', currentDir])


@cli.command()
@passGitWrapper
def ls(git):
    """List all changes."""
    #git.call(['branch']):
    git.call(['for-each-ref','refs/heads','--format=%(HEAD) %(refname:short) \t%(contents:subject)'])

@cli.command()
@passGitWrapper
@click.argument('commit', default=None, required=False)
def log(git, commit):
    """Show commit log."""
    if commit:
        # Call and ignore status, since quitting log gives a non-zero error.
        git.call(['log', '-1'] + [commit], exceptOnError=False)
    else:
        # TODO(mc): Change this if we want to support diffbases.
        # Call and ignore status, since quitting log gives a non-zero error.
        git.call(['log', '--graph', '--pretty=%C(yellow)%h%Creset%C(cyan)%d%Creset %s %C(magenta)<%an>%Creset %C(dim green)(%cr)', '--first-parent', 'master', 'HEAD'], exceptOnError=False)

@cli.command()
@notOnMaster
@passGitWrapper
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.argument('destination', type=click.Path(exists=False))
def mv(git, source, destination):
    """Move or rename a file."""
    git.call(['mv'] + list(source) + [destination])

@cli.command()
@notOnMaster
@passGitWrapper
def snapshot(git):
    """Snapshot index changes."""
    # Commit the snapshot.
    git.call(['commit', '-q', '-m', 'Snapshot commit.'])

def abort_if_false(ctx, param, value):
    if not value:
       ctx.abort()


@cli.command()
@passGitWrapper
@click.argument('path', type=click.Path(exists=False), nargs=-1)
def revert(git, path):
    """Revert local edits and undo index changes."""
    # Find the fork point for this branch.
    # TODO(mc): Change this to pass in the mainline branch that we started this
    # change from, currently it is hardcoded as master.
    forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')

    if not path:
        # TODO(mc) Make this say Revert all files in 'change'
        if click.confirm('Revert all files?', abort=True):
            #TODO(mc): Consider whether to allow a full revert if already
            # pushed to remote?
            # Revert modifications to any unstaged files
            git.call(['checkout', '--', '.'])
            # Reset file changes and index back to fork point.
            git.call(['reset', '--quiet', '--mixed', forkPoint])
            # Revert modifications in newly unstaged files due to reset.
            git.call(['checkout', '--', '.'])
    else:
        revertedFiles = []
        try:
            # For added files, reset the index and leave them untracked.
            gitDiff = splitIfNotEmpty(git.callAndGetUtf8(
                ['diff', forkPoint, '--name-status', '--'] + list(path)))
            allFiles = sorted([tuple(x.split(None, 1)) for x in gitDiff])
            groupedFiles = dict([(label, [val for _lab,val in value]) for (label, value) in
                    groupby(allFiles, lambda x:x[0])])
            if 'A' in groupedFiles:
                addedFiles = groupedFiles['A']
                # Revert adds by resetting the index (leaving the working copy).
                git.call(['reset', '--quiet', forkPoint, '--'] + addedFiles)
                revertedFiles.extend(addedFiles)
            if 'M' in groupedFiles:
                modifiedFiles = groupedFiles['M']
                # Reset any potential index differences.
                git.call(['reset', '--quiet', forkPoint, '--'] + modifiedFiles)
                # Change the working copy to the fork-point version.
                git.call(['checkout', forkPoint, '--'] + modifiedFiles)
                revertedFiles.extend(modifiedFiles)
            if 'D' in groupedFiles:
                deletedFiles = groupedFiles['D']
                # Reset any potential deletes in the index.
                git.call(['reset', '--quiet', forkPoint, '--'] + deletedFiles)
                # Recover the fork-point versions and add them to the working directory.
                git.call(['checkout', forkPoint, '--'] + deletedFiles)
                revertedFiles.extend(deletedFiles)

            currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])
            if currentBranch != 'master':
                # Find any files that require a commit to revert.
                justFiles = [x[1] for x in allFiles]
                revertDiff = git.callAndGetUtf8(['diff', '--cached', '--name-only', '--'] + justFiles)
                if revertDiff:
                    # Commit any reverts in the index.
                    revertsToCommit = revertDiff.split('\n')
                    git.call(['commit', '-m', 'Revert files.', '--'] + revertsToCommit)
                    revertedFiles.extend(revertsToCommit)
        finally:
            for revertedFile in revertedFiles:
                click.echo('Reverted ' + revertedFile)


@cli.command(help="Show changes between working tree and parent.")
@passGitWrapper
@click.argument('path', type=click.Path(exists=True), nargs=-1)
def diff(git, path):
    forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')
    git.call(['diff', forkPoint, '--'] + list(path))

def commaList(ctx, param, value):
    """Convert comma-separated string to list."""
    if not value:
        return []
    return value.split(',')

@cli.command(help="Send changes to remote and notify reviewers.")
@notOnMaster
@passGitWrapper
@click.option('-t', '--to', callback=commaList, metavar='USER1,USER2', help='List of reviewers')
@click.option('-u', '--update',  is_flag=True, help='Update commit message and files.')
def send(git, to, update):
    # Find the fork point for this branch.
    # TODO(mc): Change this to pass in the mainline branch that we started this change from,
    # currently it is hardcoded as master.
    forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')

    # Find the current branch.
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])

    revHashes = re.findall(r'([0-9a-f]+) r(\d+): .*', git.callAndGetUtf8(['log', '--pretty=%h %s', '%s..HEAD' % forkPoint.value]))

    if revHashes:
        lastRev = revHashes[0][0]
        revNumber = int(revHashes[0][1]) + 1
    else:
        lastRev = forkPoint
        revNumber = 0

    # Reset all of the changes since the last rev or fork.
    git.call(['reset', '--mixed', lastRev])
    
    (addFiles, deleteFiles) = interactiveFileList(git, 'The following files will be included in the commit.')
    if addFiles:
        git.call(['add', '--'] + addFiles, fromRoot=True)
    if deleteFiles:
        git.call(['reset', forkPoint, '--'] + deleteFiles, fromRoot=True)

    # Commit them in a new squashed commit.
    if revHashes:
        # Get the commit message from the last revision.
        desc = git.callAndGetUtf8(['log', '-1', '--pretty=%s', lastRev])

        # Strip the revision prefix.
        strippedDesc = removeRevPrefix(desc)

        # Create a new commit that strips the commit prefix.
        git.call(['commit', '-q', '--allow-empty', '-m', strippedDesc])
        
        try:
            if update:
                # Edit the commit message.
                git.call(['commit', '--allow-empty', '--amend', '-c', 'HEAD'])
        finally:
            # Make sure that we put back the revision prefix.
            desc = git.callAndGetUtf8(['log', '-1', '--pretty=%s'])
            git.call(['commit', '--allow-empty', '--amend', '-m', 'r%d: %s' % (revNumber, desc)])

    else:
        # Commit with a new commit message.
        git.call(['commit', '-q'])

        # Append r0, r1, r2, etc to the commit message.
        desc = git.callAndGetUtf8(['log', '-1', '--pretty=%s'])
        git.call(['commit', '--amend', '-m', 'r%d: %s' % (revNumber, desc)])


    # Get current user.
    user = getpass.getuser()

    remoteBranch = '%s.%s' % (user, currentBranch)

    # Send that commit to the remote server.
    git.call(['push', '--force', 'origin', '%s:%s' % (currentBranch, remoteBranch)])

    if not revHashes:
        # If this is the first call to g8 send, create a pull request.
        subject = removeRevPrefix(git.callAndGetUtf8(['log', '-1', '--pretty=%s']))
        body = git.callAndGetUtf8(['log', '-1', '--pretty=%b'])
        repo = getGithubRepo(git)
        pullRequest = repo.create_pull(
            title=subject,
            body=body,
            head=remoteBranch,
            base='master',
        )
        if to:
            # Create a review request.
            requestReview(pullRequest, to)

@cli.command(help="Merge and commit the change, then clean up.")
@notOnMaster
@passGitWrapper
@click.pass_context
def land(ctx, git):
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])

    repo = getGithubRepo(git)

    commitSha = git.callAndGetUtf8(['log', '-1', '--pretty=%H'])

    user = getpass.getuser()
    remoteBranch = '%s.%s' % (user, currentBranch)

    # Query for open pull requests in the branch.
    pullFilter = '8thwall:%s' % remoteBranch
    pagenatedRequests = repo.get_pulls(head=pullFilter)
    pullRequests = []
    for pr in pagenatedRequests:
        pullRequests.append(pr)

    if len(pullRequests) == 0:
        # Send current commit if there is no pull request.
        needsSend = True
        if not click.confirm('Land %s without review?' % currentBranch, abort=True):
            return
    elif len(pullRequests) == 1:
        pullRequest = pullRequests[0]
        # Send current commit if it doesn't match remote.
        needsSend = (pullRequest.head.sha != commitSha)
    else:
        raise click.ClickException("More than one open pull request in " + remoteBranch)
    if needsSend:
        ctx.invoke(send, to=None, update=False)
        currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])
        commitSha = git.callAndGetUtf8(['log', '-1', '--pretty=%H'])
        pullRequest = repo.get_pulls(head=pullFilter)[0]

    if pullRequest.mergeable == None:
        click.echo('Waiting for GitHub merge check')
    while pullRequest.mergeable == None:
        click.echo('=', nl=False)
        time.sleep(.1)
        pullRequest = repo.get_pulls(head=pullFilter)[0]

    if pullRequest.mergeable == False:
        raise click.ClickException("Pull request is not mergeable. Try 'g8 sync'.")

    if pullRequest.head.sha != commitSha:
        click.echo(pullRequest.head.sha)
        click.echo(commitSha)
        raise click.ClickException("Remote does not match local commit. Try 'g8 send'")

    # Merge the branch.
    subject = removeRevPrefix(git.callAndGetUtf8(['log', '-1', '--pretty=%s']))
    body = git.callAndGetUtf8(['log', '-1', '--pretty=%b'])
    mergeResult = mergeWithFixes(
        pullRequest,
        commit_title=subject,
        commit_message=body,
        merge_method='squash',
        sha=commitSha,
    )

    if not mergeResult.merged:
        raise click.ClickException("Merge failed with message %s" % (command, returncode))

    untrackedFiles = git.callAndGetUtf8([
        'ls-files', '--modified', '--others', '--exclude-standard'
    ], fromRoot=True)
    if not untrackedFiles:
        # Delete the branch if there are no files left.
        deleteFeature(git, currentBranch)
    else:
        # Find the commit this forks from.
        forkPoint = git.callAndGetUtf8Var(['merge-base', '--fork-point', 'master'], 'FORK')
        # Reset all commits that were squashed and committed.
        git.call(['reset', '--quiet', '--mixed', forkPoint])

    # Run g8 sync. Any files that were landed should be fast-forwarded and no longer modified after the sync.
    ctx.invoke(sync)

@cli.command()
@notOnMaster
@click.option('-t', '--to', callback=commaList, metavar='USER1,USER2', help='List of reviewers')
@passGitWrapper
def resend(git, to):
    """Add more reviewers to pull request."""
    currentBranch = git.callAndGetUtf8(['symbolic-ref', '--short', 'HEAD'])

    repo = getGithubRepo(git)
    commitSha = git.callAndGetUtf8(['log', '-1', '--pretty=%H'])
    subject = removeRevPrefix(git.callAndGetUtf8(['log', '-1', '--pretty=%s']))
    body = git.callAndGetUtf8(['log', '-1', '--pretty=%b'])

    user = getpass.getuser()
    remoteBranch = '%s.%s' % (user, currentBranch)

    # Assumes there is one-and-only-one pull request in this branch.
    pullFilter = '8thwall:%s' % remoteBranch
    pullRequest = repo.get_pulls(head=pullFilter)[0]
    requestReview(pullRequest, to)


if __name__ == '__main__':
    #try:
    cli(prog_name='g8')
    #except ChildProcessError as e:
        #click.echo(e)
