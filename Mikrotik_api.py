from librouteros import connect
import ssl
import socket
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
urllib3.disable_warnings()


# response = requests.get('http//94.102.126.165/rest/interface',
#                         auth=HTTPBasicAuth('admin', 'Aorbyboi1'), verify=False)
# print(response)

# class router():
#     ip = ip
#     pass


# Установка соединения с API RouterOS
connection = connect(
    username='admin', password='Aorbyboi1', host='94.102.126.165')

# Выполнение команды API
response = connection(cmd='/ip/dhcp-server/lease/print')

# Вывод результатов
for item in response:
    print(item)

# Закрытие соединения
connection.close()
