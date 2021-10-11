import json
import requests
import csv

# открытие файла для чтения
with open("f.json", "r") as read_file:
    data = json.load(read_file)

# формирование adress на основер парсинга json файла и списка files с диркториями которые нужно посетить
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