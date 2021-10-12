import json
import requests
import csv
import os.path
import re

# проверка корректности расширения и существования файла
file_name = input('название файла: ')
while not os.path.isfile(file_name) and file_name[:-5] != '.json':
    file_name = input('файл не найден или файл не является json, введите еще раз: ')

# открытие файла для чтения и обработка в случаии ошибки
with open(file_name, "r") as read_file:
    try:
        data = json.load(read_file)
    except json.decoder.JSONDecodeError:
        print('ОШИБКА: не правильный синтаксис файла json')
        raise SystemExit(1)

# проверка на наличии необходимых ключей
keys_dict = ['host', 'port', 'proto', 'files']
for i in keys_dict:
    if i not in data:
        print('ОШИБКА: отсутствует поле ' + i)
        raise SystemExit(1)

# проверка соответсвии формату(ip, host, port) данныйх из файле json
if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data['host']) is None:
    print('ОШИБКА: не правильный формат IP-адреса')
    raise SystemExit(1)
if re.match(r'http', data['proto']) is None:
    print('ОШИБКА: не правильный формат протокола')
    raise SystemExit(1)
if re.match(r"\d{,5}$", data['port']) is None:
    print('ОШИБКА: не правильный формат порта')
    raise SystemExit(1)




# формирование adress на основер парсинга json файла и списка files с диркториями которые нужно поситить
files = data['files']
adress = data['proto'] + '://' + data['host'] + ':' + data['port']

# список с словарями, которые содержат необходимые данные  из ответов GET запросов. Заполняется в цикле for
response_data = []

# отправка GET запроса и формирование списка с необходимыми данными
for i in files:
    # формирование url из спарсенных данных
    url = adress + i
    # обработка исключений связынных с get запросом
    try:
        response = requests.get(url = url)
        list_response = {'request URL': url, 'response code': response.status_code, 'comment': ''}
        if response.status_code == 301 or response.status_code == 302:
            list_response['comment'] = response.headers['Location']
    except requests.exceptions.ConnectTimeout:
        list_response = {'request URL': url, 'response code': '', 'comment': 'ConnectTimeout'}
    except requests.exceptions.ConnectionError:
        list_response = {'request URL': url, 'response code': '', 'comment': 'ConnectionRefused'}
    except requests.exceptions.InvalidURL:
        list_response = {'request URL': url, 'response code': '', 'comment': 'InvalidURL'}
    except requests.exceptions.RequestException:
        list_response = {'request URL': url, 'response code': '', 'comment': 'RequestException'}
    except requests.exceptions.TooManyRedirects:
        list_response = {'request URL': url, 'response code': '', 'comment': 'TooManyRedirects'}
    except requests.exceptions.InvalidHeader:
        list_response = {'request URL': url, 'response code': '', 'comment': 'InvalidHeader'}
    except requests.exceptions.ChunkedEncodingError:
        list_response = {'request URL': url, 'response code': '', 'comment': 'ChunkedEncodingError'}
    # Запись словаря с данными в список  response_data
    response_data.append(list_response)




# создание файла otvet.csv и запись туда данных из списка response_data
with open('otvet.csv', 'w') as csvfile:
    fieldnames = ['request URL', 'response code', 'comment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter =';')

    writer.writeheader()
    writer.writerows(response_data)