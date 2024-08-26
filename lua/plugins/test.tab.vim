function! MyTabLine()
let s = ''
for i in range(tabpagenr('$'))
let s .= '%' . (i + 1) . 'T' . '< '. (i+1) .' >'
endfor
let s .= '%#TabLine#%999Xclose'
return s
endfunction
:set tabline=%!MyTabLine()
