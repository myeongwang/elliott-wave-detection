import requests
import matplotlib.pyplot as plt
import time
from datetime import datetime
import pytz

def fetch_bybit_data(category, symbol, interval, limit, start=None, end=None):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "limit": str(limit)
    }
    
    if start:
        params["start"] = str(start)
    
    if end:
        params["end"] = str(end)

    response = requests.get(url, params=params)
    print("API 응답 내용:", response.json())
    
    if response.status_code != 200:
        print("API 호출에 실패했습니다. 상태 코드:", response.status_code)
        return None

    data = response.json()
    if "result" not in data or "list" not in data["result"]:
        print("결과(result) 키가 응답에 없습니다. 또는 list 키가 없습니다.")
        return None

    return data["result"]["list"]

    
    if start:
        params["start"] = str(start)
    
    if end:
        params["end"] = str(end)

    response = requests.get(url, params=params)
    print("API 응답 내용:", response.json())
    
    if response.status_code != 200:
        print("API 호출에 실패했습니다. 상태 코드:", response.status_code)
        return None

    data = response.json()
    if "result" not in data:
        print("결과(result) 키가 응답에 없습니다.")
        return None

    return data["result"]["list"]

def convert_to_kst(timestamp_ms):
    # 밀리초 단위의 UNIX 타임스탬프를 파싱
    timestamp_utc = datetime.utcfromtimestamp(int(timestamp_ms) / 1000.0)
    
    # UTC 시간을 KST로 변환
    kst = pytz.timezone('Asia/Seoul')
    timestamp_kst = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(kst)
    
    return timestamp_kst


def plot_chart(data):
    times = [convert_to_kst(item[0]) for item in data]  # 시간 데이터를 KST로 변환
    prices = [float(item[4]) for item in data]  # close price

    plt.figure(figsize=(15, 7))
    plt.plot(times, prices, '-o')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('BTCUSDT Price Chart (KST)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    category = "spot"
    symbol = "BTCUSDT"
    interval = "60"  # 1시간 봉
    limit = 1000

    all_data = []
    last_data = fetch_bybit_data(category, symbol, interval, limit)
    
    if last_data is None:
        print("첫 번째 API 요청에서 데이터를 받아오지 못했습니다.")
        return

    all_data.extend(last_data)

    for _ in range(4):
        start_timestamp = int(last_data[-1][0]) - (3600 * 1000)  # 마지막 데이터의 1시간 전 타임스탬프
        last_data = fetch_bybit_data(category, symbol, interval, limit, start=start_timestamp)
        
        if last_data is None:
            print(f"{_ + 2} 번째 API 요청에서 데이터를 받아오지 못했습니다.")
            break

        all_data.extend(last_data)

    plot_chart(all_data)

if __name__ == "__main__":
    main()

