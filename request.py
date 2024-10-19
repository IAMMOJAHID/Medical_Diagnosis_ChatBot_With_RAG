import requests

url = 'http://127.0.0.1:5000/predict'
data = {'input_text': 'I have a headache and fever.'}

response = requests.post(url, json=data)

print(response.json()['response'])