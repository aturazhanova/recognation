import requests

url = 'http://localhost:3000/extract-text'  # Changed port to 5001

with open('рук.jpeg', 'rb') as file:
    files = {'file': file}
    
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print(result['text'])
else:
    print("Error:", response.text)
