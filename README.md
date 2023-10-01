# elliote_wave_theory_simulation

1. simulation.py: < WebSocket API >

   실시간 데이터를 지속적으로 받아올 때 사용됩니다.
   연결이 한 번 성립되면, 그 연결을 통해 지속적으로 데이터를 받을 수 있습니다.

   위에서 제시한 websockets를 사용하는 코드는 실시간 BTCUSDT의 orderbook 데이터를 지속적으로 받아와서 출력하는 코드입니다.

2. btcusdt_data.py: <Rest Api> Bybit의 API를 통해 BTCUSDT의 가격 정보를 가져오는 파이썬 스크립트입니다.
   
   1시간 봉 data 1000개의 데이터 추출, kst(utc-9)로의 시간 변환

3. wave_detection_algorithm: 데이터에서 임펄스 파동과 수정 파동을 식별하기 위한 알고리즘.
   피크와 트로프를 감지하는 알고리즘, 그리고 이를 조합하여 파동을 찾는 알고리즘을 포함합니다.   
