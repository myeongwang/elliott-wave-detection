from datetime import datetime

timestamp = 1696078082078 / 1000  # 밀리초를 초로 변환
kst_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(kst_time)
