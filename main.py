import json
import requests
import csv

# открытие файла для чтения
with open("f.json", "r") as read_file:
    data = json.load(read_file)

files = data['files']

# список с словарями, которые содержат необходимые данные  из ответов GET запросов 
response_data = []

# отправка GET запроса и формирование списка с необходимыми данными
for i in files:
    response = requests.get(data['proto'] + '://' + data['host'] + i)
    list_response = {'request URL': response.url, 'response code': response.status_code, 'comment': ' '}
    response_data.append(list_response)

# создание файла otvet.csv и запись туда данных из списка response_data
with open('otvet.csv', 'w') as csvfile:
    fieldnames = ['request URL', 'response code', 'comment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter =';')

    writer.writeheader()
    writer.writerows(response_data)