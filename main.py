from flask import Flask, render_template, url_for, request, send_file
from resourse.hash_code import get_hash
from resourse.db_module import DBLinks
import os
from flask_cors import CORS

from selenium import webdriver
import io

# подключение к базе данных
db = DBLinks()

app = Flask(__name__)
CORS(app)


@app.route('/ping')
def ping():
    """
    Проверка запуска сервера
    :return: ok - работает
    """
    return '{"message": "ok"}'


@app.route('/')
@app.route('/index.html')
def index():
    """
    Главная страница (для работы с ссылками)
    :return: страница
    """
    return render_template("index.html")


@app.route('/new_link/', methods=['GET', 'POST'])
def new_link():
    """
    Создание короткого хэша для полной ссылки, запись в базу данных. Принимает полную ссылку.
    :return: Возвращает параметр error при возникновении ошибки, link - короткая ссылка создана
    """
    print('Kva')
    print(request.url_root)
    if request.method == 'POST':
        long_link = request.form.get('long_link', default=None, type=None)
    else:
        long_link = request.args.get('long_link', default=None, type=None)

    if long_link is not None:
        hash_link = get_hash(8)
        new_l = db.new_link(long_link, hash_link)
        if new_l != 505:
            hash_link = request.url_root + 'link/' + hash_link
            return '{"link": "' + hash_link + '"}'
        else:
            return '{"error": "database"}'
    else:
        return '{"error": "data"}'


@app.route('/link/<string:hash_link>')
def link(hash_link: str):
    """
    Производит редирект
    :param hash_link: хэш-код для короткой ссылки
    :return: 505 - ошибка базы данных,
            False - ссылка отсутствует,
            соответствующая длинная ссылка
    """
    print(hash_link)
    get_link = db.get_link(hash_link)

    if not get_link:
        return render_template("error_404.html")
    elif get_link == 505:
        return render_template("error_db.html")
    else:
        return f'<script>window.location.replace("{get_link}");</script>'


@app.route('/screen/', methods=['GET', 'POST'])
def screen_link():
    """
    Получает короткую ссылку и делает скриншот этой страницы.
    :return: Возвращает параметр error при возникновении ошибки, link - короткая ссылка создана
    """
    if request.method == 'POST':
        long_link = request.form.get('long_link', default=None, type=None)
    else:
        long_link = request.args.get('long_link', default=None, type=None)

    if long_link is not None:
        browser = webdriver.Edge()
        browser.get(long_link)

        # Получение скриншота страницы в виде байтового потока
        screenshot = browser.get_screenshot_as_png()

        # Закрытие браузера
        browser.quit()

        # Создание байтового потока в памяти
        stream = io.BytesIO(screenshot)

        # Возвращение скриншота в виде ответа на HTTP-запрос
        return send_file(stream, mimetype='image/png')
    else:
        return '{"error": "data"}'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=4000))
    
