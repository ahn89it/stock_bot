
import KIS_Common as Common
import KIS_API_Helper_KR as KisKR
import json

import market_search
import time

Common.SetChangeMode("VIRTUAL")
date_kr = Common.GetNowDateStr("KR", "NONE")
print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")



# 종목 코드가 담긴 JSON 파일 이름
input_json_filename = f"target_stock_code_{date_kr}.json"

# JSON 파일에서 종목 코드 리스트 읽기
with open(input_json_filename, "r", encoding="utf-8") as json_file:
    stock_code_list = json.load(json_file)

print(f"읽은 종목 코드 리스트: {stock_code_list}")
print(f"읽은 종목 코드 리스트: {stock_code_list[0]}")
target_price_list = []
# 각 종목 코드에 대해 GetOhlcv 호출
for stock_code in stock_code_list:
    if(market_search.get_market_type(stock_code)=='kospi'):
        nanugi=2.5
    else:
        nanugi=2
    # GetOhlcv 함수에 종목 코드를 넣고 처리 (2일치 데이터를 가져옴)
    df = Common.GetOhlcv("KR", stock_code, 4)
    #print(df)
    start_price = df['open'].iloc[-1] #시가
    high_price = df['high'].iloc[-2] #전날 고가
    low_price = df['low'].iloc[-2]  # 전날 저가
    target_price = start_price + (high_price - low_price) / nanugi
    adjust_target_price = KisKR.PriceAdjust(target_price, stock_code) #호가 단위에 맞게 target_price 가격 조정!!!!
    target_price_list.append(adjust_target_price )
    time.sleep(2)
    #print(f"{stock_code} 종목의 OHLCV 데이터:\n", target_price)


print(target_price_list)
print(type(target_price_list))

out_json_filename = f"target_price_list_{date_kr}.json"
with open(out_json_filename, "w", encoding="utf-8") as json_file_:
    json.dump(target_price_list, json_file_, ensure_ascii=False, indent=4)




"""
*매수 프로세스
(1) -토큰값 파일저장 (stock_token_real.jsaon / stock_token_virtual.json)
    -크론탭은 00시 넘어서
    -token_save.py
(2) -목표 종목 리스트 선정 -> 종목리스트 파일 저장
    -파일제목 : target_stock_code_날짜
    -크론탭은 00시 넘어서
    -조건에 만족하는 종목코드들이 없을때는 빈 리스트가 저장됨 
    -stock_code_save.py
(3) -(2)에서 넘어온 파일의 리스트 길이가 0이면 !종료!
    -09시00분 or 09시01분 크론탭
    -'당일_시작가', '전날_고가', '전날_저가' 확인 -> 코스피/코스닥 확인-> 목표가 계산 -> 리스트파일저장
    -파일제목 : target_price_list_날짜
    -market_search.py : 종목이 코스닥인지 코스피인지 확인하는 함수 
    -target_price_save.py
(4) -실시간 현재가 - 목표가 일치한지 확인 -> 일치하면 목표가로 매수 주문 
    -1초마다 크론탭이나. while문 
    -(1),(2)파일 read

※
*매도 프로세스
(1) 당일 날짜 check -> 5일전 파일 종목리스트 read
(2) 종목리스트 시가 매도
"""
