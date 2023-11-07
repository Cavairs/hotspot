from flask import Flask, request, render_template
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from librouteros import connect


# Создание экземпляра класса Flask
app = Flask(__name__)

# Создание клиента Radius
radius_client = Client(server="radius_server_ip", secret="radius_secret_key",
                       dict=Dictionary("path_to_radius_dictionary"))

# Создание клиента RouterOS
routeros_connection = connect(
    username='admin', password='password', host='192.168.0.1')

# Функция для обработки авторизации


def handle_login(username, password):
    # Формирование запроса к серверу Radius
    radius_client.CreateAuthPacket(code=1, User_Name=username)
    radius_client["User-Password"] = radius_client.PwCrypt(password)

    # Отправка запроса к серверу Radius
    radius_response = radius_client.SendPacket()

    # Обработка ответа сервера Radius
    if radius_response.code == 2:
        # Авторизация успешна

        # Выполнение команды API MikroTik RouterOS для разрешения доступа пользователя к интернету
        routeros_connection(cmd='/ip/hotspot/user/set',
                            _id=username,
                            disabled='no')

        return True
    else:
        # Авторизация не удалась
        return False

# Обработка GET-запроса для отображения страницы авторизации


@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

# Обработка POST-запроса от страницы авторизации


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Вызов функции обработки авторизации
        if handle_login(username, password):
            # Авторизация успешна, выполните необходимые действия
            return "Авторизация успешна"
        else:
            # Авторизация не удалась, выполните соответствующие действия
            return "Авторизация не удалась"


if __name__ == '__main__':
    app.run()
