from flask import Flask
import psycopg2
from config import dbname, user, password, host
import requests
import json


# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# лицевой счет
get_ls = 843575
# password = input('Введите пароль:')

url = 'https://api.cpx.ru/ask.php'
payload = {'id':  get_ls}
try:
    response = requests.get(url, params=payload)
    data = response.json()
    abonent_meta_list = data['abonent']
    abonent_find = abonent_meta_list[0]
    ab_id = int(abonent_find['AB_ID'])
    ab_balanse = abonent_find['ACC_CURRENT_BALANCE']
    abonent_sevisce_list = data['ct_users']
    abonent_sevisce_find = abonent_sevisce_list[0]
    abonent_sevisce_user_in = abonent_sevisce_find['ct_user_services']
    abonent_sevisce_user_out = abonent_sevisce_user_in[2]
    ab_lk_password = abonent_sevisce_user_out['USS_PASSWORD']
except KeyError:
    pass
except requests.exceptions.ConnectionError:
    pass
except Exception:
    pass

# print(ab_id, ab_balanse, ab_lk_password)


try:
    # Подключенеи к бд
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )
    connection.autocommit = True
    # Курсор
    # cursor = connection.cursor()     если используем такой подкод то  в блоке finaly нужно закрыть обьект cursor (      cursor.close()      )

    with connection.cursor() as cursor:
        # метод execute в обьекте крусор позволяет делать обращения к дазе данных
        # cursor.execute(
        #     "SELECT version();"
        # )
        find_select = 'SELECT personal_account FROM hotspot_list WHERE personal_account = %s'
        params = (ab_id,)
        cursor.execute(find_select, params)
        result_fetchone = cursor.fetchone()
        if result_fetchone is not None and ab_lk_password == ab_lk_password:
            print(ab_lk_password)
            print('Такое уже есть ')

        # elif result_fetchone is not None and ab_lk_password != ab_lk_password:   

        else:
            query = 'INSERT INTO hotspot_list (personal_account, password) VALUES (%s, %s);'
            data = (ab_id, ab_lk_password)
            cursor.execute(query, data)
        # query = 'INSERT INTO user_hotspot (personal_account, password_account) VALUES (%s, %s);'
        # data = (ab_id, ab_lk_password)
        # cursor.execute(query, data)

except Exception as ex:
    print('Error', ex)
    

finally:
    if connection:
        # cursor.close()  закрываем если использунем в виде переменной .. для менеджера контекста with это не нужно .
        connection.close()
        print('[INFO] SQL connect close')
