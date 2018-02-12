$(function () {
 
    $('.spoiler-trigger').on('click', function (e) { 
        e.preventDefault();
        $(this).toggleClass('active');
        $(this).parent().find('.spoiler-block').first().slideToggle(300);
    })
   
    //<!-- https://github.com/caldwell/renderjson -->
    renderjson.set_icons('[+]', '[-]')
    var elements = document.getElementsByClassName("json"),
        content;
    for(var i = 0; i < elements.length; i++) {
        content = elements[i].innerHTML;
        elements[i].innerHTML = '';
        elements[i].appendChild(renderjson(JSON.parse(content)));
    }
})





