var timer;

links = new Vue({
    el: '#form',
    data: {
        full_link: '',
        short_link: '',
        img_link: 'https://mykaleidoscope.ru/uploads/posts/2018-05/1527595743_vy_tolko_poslushayte_kak_myaukayut_eti_kotyata_.jpg'
    }
});

// нажатие на кнопку копирования - копирование в буфер, показ уведомления
$("#copy_button").click(function() {
    $('#short_link').select();
    document.execCommand("copy");
    // сбрасываем выделение после копирования
    window.getSelection().removeAllRanges();

    $('#copy').addClass('show');
    timer = setTimeout(close_copy, 3000);
});

// активация подсказок bootstrap
$(function() {
    $('[data-toggle="tooltip"]').tooltip()
})

// скрытие уведомления через время или по закрытию
function close_copy(){
    clearInterval(timer);
    $('#copy').removeClass('show');
}

$("#form").submit(function(){
    // убирает отправку формы, но оставляет валидацию
    event.preventDefault();

    get_link();
});

/* получение короткой ссылки */
function get_link(){
    $.ajax({
        method: "GET",
        url: "http://127.0.0.1:4000/new_link/",
        data: {long_link: links.$data.full_link}
    })
    .done(function(response){
        // Получение данных в формате JSON
        var data = JSON.parse(response);

        // Проверка наличия конкретного параметра
        if (data.hasOwnProperty("link")) {
            // параметр "link" присутствует
            links.$data.short_link = data.link;

            // картинка котика на ожидание
            links.$data.img_link = 'static/img/cat2.gif';

            // отправка запроса на скриншот
            get_screen_link();
        } else {
            // если параметра нет, то произошла ошибка
            alert("Error!");
        }
    });
}


/* получение скриншота страницы */
function get_screen_link(){
    $.ajax({
        method: "GET",
        url: "http://127.0.0.1:4000/screen/",
        data: {long_link: links.$data.full_link},
        xhrFields: {
            responseType: 'blob'
        },
        success: function(blob) {
            // Создание объекта URL для полученного Blob
            var imageUrl = URL.createObjectURL(blob);

            links.$data.img_link = imageUrl;
        }
    });
}
