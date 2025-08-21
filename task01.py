import requests
import time
from datetime import datetime
from CLI_color import *

url = f"https://yandex.com/time/sync.json?geo=213"


def GetJson(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"{color_red}Ошибка при выполнении запроса: {e}{color_end}")


def OutputData(data) -> datetime:
    print(data)
    server_timestamp = datetime.fromtimestamp(
        (data["time"] - data["clocks"]["213"]["offset"]) / 1000
    )
    timezone_UTC = data["clocks"]["213"]["offsetString"]
    timezone_name = data["clocks"]["213"]["name"]
    readeble_time = server_timestamp.strftime("%d-%m-%Y %H:%M:%S")
    print(
        f"{color_orange}Время сервера и временная зона{color_end}\n",
        readeble_time,
        timezone_UTC,
        timezone_name,
    )
    return server_timestamp


def main():
    deltas = []
    for i in range(5):
        local_time = datetime.now()
        jsonfile = GetJson(url)
        server_time = OutputData(jsonfile)
        delta_ms = (local_time - server_time).total_seconds()
        print(f"{color_orange}Delta time:{color_end} {delta_ms: .2f} s")
        if delta_ms is not None:
            deltas.append(delta_ms)
        time.sleep(1)
    if deltas:
        avg_delta = sum(deltas) / len(deltas)
        print(f"{color_green}Средняя дельта:{color_end} {avg_delta:.2f} мс")


if __name__ == "__main__":
    main()
