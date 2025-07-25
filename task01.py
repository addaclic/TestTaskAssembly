import requests
import time
from datetime import datetime

url = f"https://yandex.com/time/sync.json?geo=213"


def GetJson(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


def OutputData(data) -> datetime:
    print(data)
    server_timestamp = datetime.fromtimestamp(
        (data["time"] - data["clocks"]["213"]["offset"]) / 1000
    )
    timezone_UTC = data["clocks"]["213"]["offsetString"]
    timezone_name = data["clocks"]["213"]["name"]
    readeble_time = server_timestamp.strftime("%d-%m-%Y %H:%M:%S")
    print(
        f"\033[38;2;201;100;59mВремя сервера и временная зона\033[0m",
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
        print(f"\033[38;2;201;100;59mDelta time:\033[0m {delta_ms: .2f} s")
        if delta_ms is not None:
            deltas.append(delta_ms)
        time.sleep(1)
    if deltas:
        avg_delta = sum(deltas) / len(deltas)
        print(f"\033[32mСредняя дельта:\033[0m {avg_delta:.2f} мс")


if __name__ == "__main__":
    main()
