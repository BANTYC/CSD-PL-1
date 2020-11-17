import requests

server_address = 'http://localhost:8000/'

response = requests.get(server_address)
print(response)

print(response.text)

