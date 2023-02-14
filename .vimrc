set number
set tabstop=2
set shiftwidth=2
set expandtab
set foldlevel=99
set ts=2
nnoremap <space> za

set foldmethod=indent
nnoremap <space> za
vnoremap <space> zf

autocmd FileType make set noexpandtab shiftwidth=8 softtabstop=0
autocmd BufNewFile,BufRead *.go setlocal noexpandtab tabstop=4 shiftwidth=4
autocmd BufNewFile,BufRead *.py setlocal expandtab tabstop=4 shiftwidth=4
autocmd BufNewFile,BufRead *.tsx,*.jsx set filetype=typescriptreact
autocmd BufNewFile,BufRead *.yml setlocal expandtab tabstop=2 shiftwidth=2
autocmd BufNewFile,BufRead *.ts,*.js setlocal expandtab tabstop=2 shiftwidth=2
