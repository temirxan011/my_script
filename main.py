#!/usr/bin/python
import json
import csv
import os.path
import re
from sys import argv
import requests


# function to open json file and check data
def reading_file():
    # checking the correctness of the extension and the existence of the file
    try:
        file_name = argv[1]
    except:
        print('ERROR: missing argument <file_name>')
        raise SystemExit(0)
    if not os.path.isfile(file_name) and file_name[:-5] != '.json':
       print('ERROR: file not found or file is not json')
       raise SystemExit(0)

    # opening a file for reading and processing in case of an error
    with open(file_name, "r") as read_file:
        try:
            data = json.load(read_file)
        except:
            print('ERROR: file is not json or json file syntax not correct')
            raise SystemExit(0)

    # checking for the necessary keys
    keys_dict = ['host', 'port', 'proto', 'files']
    if len(data) == 4:
        for i in keys_dict:
            if i not in data:
                print('ERROR: missing field ' + i)
                raise SystemExit(0)
    else:
        print('ERROR: the number of fields is not correct')
        raise SystemExit(0)

    # check for compliance with the format (ip, host, port) given from the json file
    if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', str(data['host'])) is None:
        print('ERROR: not correct IP address format')
        raise SystemExit(0)
    if re.match(r'http', str(data['proto'])) is None:
        print('ERROR: incorrect protocol format')
        raise SystemExit(0)
    if re.match(r"\d{1,5}$", str(data['port'])) is None:
        print('ERROR: not correct port format')
        raise SystemExit(1)
    if type(data['files']) != list:
        print('ERROR: values by key files is not a list')
        raise SystemExit(0)
    return data


# function for sending get requests
def sending_requests(data):
    # formation of an adress based on parsing a json file and a list of files with directories that need to be visited
    directory_list = data['files']
    provisional_address = str(data['proto']) + '://' + str(data['host']) + ':' + str(data['port'])

    # a list with dictionaries that contain the necessary data from the responses of GET requests. Filled in for loop
    response_data = []

    # sending a GET request and forming a list with the necessary data
    for i in directory_list:
        # forming url from parsed data
        url = provisional_address + str(i)
        # handle exceptions associated with a get request
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
        # Writing a dictionary with data to the response_data list
        response_data.append(list_response)
    return response_data


# functions for writing data in csv format
def file_creation_csv(response_data):
    # creating a otvet.csv file and writing data there from the response_data list
    try:
        with open('report.csv', 'w') as csv_file:
            fieldnames = ['request URL', 'response code', 'comment']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames,  delimiter =';')

            writer.writeheader()
            writer.writerows(response_data)
    except IOError:
        print('ERROR: Permission denied')
        raise SystemExit(0)



main_data = reading_file()
main_response_data = sending_requests(main_data)
file_creation_csv(main_response_data)