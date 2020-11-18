import requests
import json

tz = 'Africa/Abidjan'
date_with_tz = {
    "start": {"date": "12.20.2021 22:21:05", "tz": "EST"},
    "end": {"date": "12:30pm 2020-12-01", "tz": "Europe/Moscow"}
}
date_no_tz = {
    "start": {"date": "12.20.2021 22:21:05"},
    "end": {"date": "12:30pm 2020-12-01"}
}

server_address = 'http://localhost:8000/'

print('Task 1:')
get = requests.get(server_address)
print(get.text)

print('Task 2:')
get = requests.get(server_address + tz)
print(get.text)

print('Task 3:')
data = json.dumps({'tz': tz})
post = requests.post(server_address + 'api/v1/time', data)
print(post.text)

print('Task 4:')
data = json.dumps({'tz': tz})
post = requests.post(server_address + 'api/v1/date', data)
print(post.text)

print('Task 5 test 1:')
data = json.dumps({
    'start': date_with_tz['start'],
    'end': date_with_tz['end']
})
post = requests.post(server_address + 'api/v1/datediff', data)
print(post.text)

print('Task 5 test 2:')
data = json.dumps({
    'start': date_with_tz['start'],
    'end': date_no_tz['end']
})
post = requests.post(server_address + 'api/v1/datediff', data)
print(post.text)

print('Task 5 test 3')
data = json.dumps({
    'start': date_no_tz['start'],
    'end': date_no_tz['end']
})
post = requests.post(server_address + 'api/v1/datediff', data)
print(post.text)