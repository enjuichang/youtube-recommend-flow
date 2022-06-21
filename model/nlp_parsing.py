
import requests


def getGameTitle(title):
    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }
    json_data = {
        'text': title,
    }
    response = requests.post('http://localhost:5000/gpt3', headers=headers, json=json_data)
    return str(response.content)[3:-4]

if __name__ == "__main__": 
    print(getGameTitle("Minecraft - Double Life #1: Stuck Together Forever"))