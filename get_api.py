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
get_ls = 831458
# password = input('Введите пароль:')

url = 'https://api.cpx.ru/ask.php'
payload = {'id':  get_ls}

response = requests.get(url, params=payload)
data = response.json()
print(data)
abonent_meta_list = data['abonent']
abonent_find = abonent_meta_list[0]
ab_id = int(abonent_find['AB_ID'])
ab_balanse = abonent_find['ACC_CURRENT_BALANCE']
abonent_sevisce_list = data['ct_users']
abonent_sevisce_find = abonent_sevisce_list[0]
abonent_sevisce_user_in = abonent_sevisce_find['ct_user_services']
abonent_sevisce_user_out = abonent_sevisce_user_in[2]
ab_lk_password = abonent_sevisce_user_out['USS_PASSWORD']


print(ab_id, ab_balanse, ab_lk_password)


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
        find_select = 'SELECT personal_account FROM user_hotspot WHERE personal_account = %(value)s'
        params = {'value': ab_id}
        cursor.execute(find_select, params)
        result_fetchone = cursor.fetchone()
        print(result_fetchone)
        result = result_fetchone[0]

        if result == ab_id:
            print('Такое уже есть ')

        elif result == None:
            query = 'INSERT INTO user_hotspot (personal_account, password_account) VALUES (%s, %s);'
            data = (ab_id, ab_lk_password)
            cursor.execute(query, data)
        # query = 'INSERT INTO user_hotspot (personal_account, password_account) VALUES (%s, %s);'
        # data = (ab_id, ab_lk_password)
        # cursor.execute(query, data)

except Exception as ex:
    print('Error', ex)
    pass

finally:
    if connection:
        # cursor.close()  закрываем если использунем в виде переменной .. для менеджера контекста with это не нужно .
        connection.close()
        print('[INFO] SQL connect close')
