import requests
import time
from datetime import datetime
import json

url = f"https://yandex.com/time/sync.json?geo=213"


def GetJson(url: str):
    local_time = time.time()
    try:
        # local_time = datetime.now()
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        server_time = data['time']/1000
        print(f'Local  time', local_time)
        print(f'Server time', server_time)
        # server_time = datetime.fromtimestamp(data["time"]/1000)
        timezone_name = data["clocks"]["213"]["name"]

        print(data)
        print(f"Время сервера и временная зона",
              datetime.fromtimestamp(server_time), timezone_name)

        delta = local_time - data["time"]/1000

        print(f"Delta time:", delta)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


def main():
    GetJson(url)


if __name__ == "__main__":
    main()
