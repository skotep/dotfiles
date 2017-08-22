set nocompatible
filetype off
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" Your Vundle plugins go here.
"Plugin 'Shougo/vimproc.vim'          " Force install a dependency of tsuquyomi.
Plugin 'leafgarland/typescript-vim'  " enables TypeScript syntax-highlighting.
"Plugin 'Quramy/tsuquyomi'            " enables TypeScript auto-completion.
call vundle#end()

" TypeScript plugin setup
let g:tsuquyomi_use_dev_node_module = 2
let g:tsuquyomi_tsserver_path = '/google/src/head/depot/google3/third_party/javascript/node_modules/typescript/stable/lib/tsserver.js'

nnoremap <silent> <leader>h :echo tsuquyomi#hint()<CR>

if !empty(glob("/usr/share/vim/google/google.vim"))
source /usr/share/vim/google/google.vim

" Plugin configuration.
" See http://google3/devtools/editors/vim/examples/ for example configurations
" and http://go/vim/plugins for more information about vim plugins at Google.

" Plugin loading is commented out below - uncomment the plugins you'd like to
" load.

" Load google's formatting plugins (http://go/vim/plugins/codefmt-google).
" The default mapping is \= (or <leader>= if g:mapleader has a custom value),
" with
" - \== formatting the current line or selected lines in visual mode
"   (:FormatLines).
" - \=b formatting the full buffer (:FormatCode).
"
" To bind :FormatLines to the same key in insert and normal mode, add:
"   noremap <C-K> :FormatLines<CR>
"   inoremap <C-K> <C-O>:FormatLines<CR>
"Glug codefmt plugin[mappings] gofmt_executable="goimports"
"Glug codefmt-google

" Enable autoformatting on save for the languages at Google that enforce
" formatting, and for which all checked-in code is already conforming (thus,
" autoformatting will never change unrelated lines in a file).
"augroup autoformat_settings
"  " For BUILD files and Go all of Google's files must be formatted.
"  autocmd FileType bzl AutoFormatBuffer buildifier
"  autocmd FileType go AutoFormatBuffer gofmt
"augroup END

" Load YCM (http://go/ycm) for semantic auto-completion and quick syntax
" error checking. Pulls in a google3-enabled version of YCM itself and
" a google3-specific default configuration.
Glug youcompleteme-google

" Load the automated blaze dependency integration for Go.
" Note: for Go, blazedeps uses the Go team's glaze tool, which is fully
" supported by the Go team; for other languages. Note that the plugin is
" currently unsupported for other languages.
"Glug blazedeps auto_filetypes=`['go']`

" Load piper integration (http://wiki/Main/VimPerforce).
"Glug piper plugin[mappings]

" Load the Critique integration. Use :h critique for more details.
"Glug critique plugin[mappings]

" Load blaze integration (http://go/blazevim).
"Glug blaze plugin[mappings]

" Load the syntastic plugin (http://go/vim/plugins/syntastic-google).
" Note: this requires installing the upstream syntastic plugin from
" https://github.com/scrooloose/syntastic.
"Glug syntastic-google

" Load the ultisnips plugin (http://go/ultisnips).
" Note: this requires installing the upstream ultisnips plugin from
" https://github.com/SirVer/ultisnips.
"Glug ultisnips-google
"
"
"==================================="
" Load and Configure Google Plugins "
"==================================="
" For more plugins, see go/vim/plugins

" :PiperSelectActiveFiles comes by default from google.vim. It's so useful that
" we map it to <leader>p (i.e., ,p).
" Use :h piper for more details about the piper integration
noremap <unique> <leader>p :PiperSelectActiveFiles<CR>

" Load the blaze plugins, with the ,b prefix on all commands.
" Thus, to Blaze build, you can do <leader>bb.
" Since we've set the mapleader to ',' above, this should be ,bb in practice
Glug blaze plugin[mappings]='<leader>b'

" Loads youcompleteme, the awesomest autocompletion engine.
" See go/ycm for more details.
Glug youcompleteme-google

" GTImporter is a script that uses GTags to find and sort Java imports. This is
" only useful for Java, so you will want to remove these lines if you don't use
" Java. You can use with codefmt to auto-sort on write with:
" autocmd FileType java AutoFormatBuffer gtimporter
Glug gtimporter
" Import the work under the cursor
nnoremap <leader>si :GtImporter<CR>
" Sort the imports in the (java) file
nnoremap <leader>ss :GtImporterSort<CR>

" Load the code formatting plugin. We first load the open-source version. Then,
" we load the internal google settings. Then, we automatically enable formatting
" when we write the file for Go, BUILD, proto, and c/cpp files.
" Use :h codefmt-google or :h codefmt for more details.
Glug codefmt
Glug codefmt-google

" Wrap autocmds inside an augroup to protect against reloading this script.
" For more details, see:
" http://learnvimscriptthehardway.stevelosh.com/chapters/14.html
augroup autoformat
  autocmd!
  " Autoformat BUILD files on write.
  autocmd FileType bzl AutoFormatBuffer buildifier
  " Autoformat go files on write.
  autocmd FileType go AutoFormatBuffer gofmt
  " Autoformat proto files on write.
  autocmd FileType proto AutoFormatBuffer clang-format
  " Autoformat c and c++ files on write.
  autocmd FileType c,cpp AutoFormatBuffer clang-format
augroup END

" Load the G4 plugin, which allows G4MoveFile, G4Edit, G4Pending, etc.
" Use :h g4 for more details about this plugin
Glug g4

" Load the Related Files plugin. Use :h relatedfiles for more details
Glug relatedfiles
nnoremap <unique> <leader>rf :RelatedFilesWindow<CR>

" Enable the corpweb plugin, which allows us to open codesearch from vim
Glug corpweb
" search in critique for the word under the cursor
nnoremap <leader>ws :CorpWebCs <cword> <Cr>
" search in critique for the current file
nnoremap <leader>wf :CorpWebCsFile<CR>

" Load the Critique integration. Use :h critique for more details
Glug critique

endif

" All of your plugins must be added before the following line.

" Enable file type based indent configuration and syntax highlighting.
" Note that when code is pasted via the terminal, vim by default does not detect
" that the code is pasted (as opposed to when using vim's paste mappings), which
" leads to incorrect indentation when indent mode is on.
" To work around this, use ":set paste" / ":set nopaste" to toggle paste mode.
" You can also use a plugin to:
" - enter insert mode with paste (https://github.com/tpope/vim-unimpaired)
" - auto-detect pasting (https://github.com/ConradIrwin/vim-bracketed-paste)
filetype plugin indent on
syntax on
set number
set list listchars=tab:»\ ,trail:°
set tabstop=4
set shiftwidth=4
"set expandtab
set hlsearch
nnoremap <s-k> <CR>

"let mapleader=';'
"

