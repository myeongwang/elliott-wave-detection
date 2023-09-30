import time
import hmac
import hashlib
from ratelimiter import RateLimiter
import bybit
import websockets
import asyncio
import json

# 초당 최대 10개의 요청을 허용하는 제한자 생성
rate_limiter = RateLimiter(max_calls=10, period=1)

@rate_limiter
def get_bybit_client():
    return bybit.bybit(test=False, api_key="3v4hhwNBkaT491H6yM", api_secret="eQH0gyDtKo2eZgp7qYmXnh0Wob47lZPR7Poe")

symbol = "BTCUSDT"

async def send_ping(ws):
    while True:
        # 20초마다 핑 메시지 전송
        await asyncio.sleep(20)
        ping_msg = {"op": "ping"}
        await ws.send(json.dumps(ping_msg))

async def main():
    uri = "wss://stream.bybit.com/v5/public/linear"
    async with websockets.connect(uri) as ws:
        
        # 핑 메시지 전송 작업 시작
        asyncio.create_task(send_ping(ws))
        
        # 웹소켓 시작
        subscribe_message = {"op": "subscribe", "args": [f"orderbook.1.{symbol}"]}  # 주제 변경
        await ws.send(json.dumps(subscribe_message))

        # 실시간 데이터 수신 및 처리
        while True:
            response = await ws.recv()
            print(response)

# 비동기 main 함수 실행
asyncio.run(main())
