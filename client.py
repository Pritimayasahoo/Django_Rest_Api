import requests

response = requests.get('http://127.0.0.1:8000/student/2')

print(response.status_code)
print(response.json())

