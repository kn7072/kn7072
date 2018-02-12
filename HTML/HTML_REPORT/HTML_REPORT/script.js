$(function () {
    function xxx (e) {
        e.stopPropagation();
        $(this).css({"display": "none"});
        $(this).siblings('.object').css({"display": "inline-block"});
     }
    $('.object').on('click', xxx); 
   $('.spoiler-trigger').on('click', function (e) {
      e.preventDefault();
      $(this).toggleClass('active');
      $(this).parent().find('.spoiler-block').first().slideToggle(300);
   });

   window.onpopstate = function (event) {
      openSpoiler();
   };

   window.onblur = function (event) {
      openSpoiler();
   };

   //<!-- https://github.com/caldwell/renderjson -->
   renderjson.set_icons('[+]', '[-]')
   var elements = document.getElementsByClassName("json"),
      content;
   for (var i = 0; i < elements.length; i++) {
      content = elements[i].innerHTML;
      elements[i].innerHTML = '';
      elements[i].appendChild(renderjson(JSON.parse(content)));
   }

   function openSpoiler() {
      var
         a = $('a[name =' + document.location.hash.substr(1) + ']');

      a.addClass('active');
      a.siblings('.spoiler-block').css({"display": "block"});
      a.closest('.spoiler-block').css({"display": "block"});
   }

//    var diff2htmlUi = new Diff2HtmlUI({diff: diffString});
//    diff2htmlUi.draw('html-target-elem', {inputFormat: 'json', showFiles: true, matching: 'lines'});
// var xxx = ' templates = extractFiles(options.argv.remain) \
// .map(function(file) {   \
//     -                var openedFile = fs.readFileSync(file, \'utf-8\');\
//     +                var openedFile = fs.readFileSync(file, \'utf-8\').trim();\
//     var name'
// var c = 'ВИ.ПолучитьСостояниеВнешнегоИнтерфейса\n\njson1 не входит в json2: \n  {\n     "id": 0, \n     "jsonrpc": "2.0", \n     "result": {\n        "d": {\n-          "ВерсияИнтерфейса": "11111111", \n?                                 ^^^^^^\n+          "ВерсияИнтерфейса": "1.16.7", \n?                                + ^^^\n-          "ДатаВремяЗапроса": "000000", \n?                                   ^\n+          "ДатаВремяЗапроса": "07-02-2018 13:30:40", \n?                                ++ +++ +++++++ ^^\n-          "СостояниеИнтерфейса": "333333"\n?                                  ^^^^^^\n+          "СостояниеИнтерфейса": "Готов"\n?                                  ^^^^^\n        }, \n        "s": {\n           "ВерсияИнтерфейса": "Строка", \n           "ДатаВремяЗапроса": "Строка", \n           "СостояниеИнтерфейса": "Строка"\n        }\n     }\n  }'
// var e = 'diff --git a/1.txt b/2.txt\nindex f4f5af4..448c5bd 100644\n--- a/1.txt\n+++ b/2.txt\n@@ -4,13 +4,13 @@\n "params":\n    {"ВходныеДанные":\n       {"s":\n-         {"ИдентификаторПакетаДокументов":"Строка",\n+         {"ИдентификаторПакетаДокументов":"cccc",\n           "ОтпечатокСертификата":"Строка",\n           "ТекстУточнения":"Строка"},\n        "d":\n          {"ИдентификаторПакетаДокументов":"$_TEST_3_GUID_DOC",\n           "ОтпечатокСертификата":"$_SERVER_CERT",\n-          "ТекстУточнения":"Тестирование отклонения серверным ключом"}\n+          "ТекстУточнения":"Тестирование отdddddddddия серверным ключом"}\n       }\n    },\n "id":0'

//     var diff2htmlUi = new Diff2HtmlUI({diff: e });
//     diff2htmlUi.draw('#diff_text', {inputFormat: 'json', showFiles: true, matching: 'lines'});
//     diff2htmlUi.highlightCode('#diff_text');
// //line-by-line
// $("#diff_text").append(diff2htmlUi);    

})





