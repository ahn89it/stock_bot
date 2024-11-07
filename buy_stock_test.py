import KIS_Common as Common
import KIS_API_Helper_KR as KisKR
import json
import time  # 1초마다 실행하기 위해 추가

Common.SetChangeMode("VIRTUAL")
date_kr = Common.GetNowDateStr("KR", "NONE")
print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")

# 종목 코드가 담긴 JSON 파일 이름
input_json_filename = f"target_stock_code_{date_kr}.json"
input_json_filename2 = f"target_price_list_{date_kr}.json"

# 종목 코드가 담긴 JSON 파일에서 종목 코드 리스트 읽기
with open(input_json_filename, "r", encoding="utf-8") as json_file:
    stock_code_list = json.load(json_file)
with open(input_json_filename2, "r", encoding="utf-8") as json_file:
    price_list = json.load(json_file)

# 각 종목당 투자할 금액!
StockMoney = 1000000
print("투자할 금액 :", str(format(round(StockMoney), ',')))

list_len = len(stock_code_list)
check_list = []  # 주문 플래그 리스트 초기화

# 무한 루프를 사용하여 1초마다 반복 실행
while True:
    for i in range(list_len):
        current_price = KisKR.GetCurrentPrice(stock_code_list[i])
        amt = StockMoney / current_price

        # 조건을 만족하면 주문을 넣고, check_list 플래그를 1로 변경
        if (current_price >= price_list[i]) and (check_list[i] == 0):
            check_list[i] = 1
            KisKR.MakeBuyLimitOrder(stock_code_list[i], amt, price_list[i], True, "NO")
            #print(f"종목 코드: {stock_code_list[i]}, 주문 가격: {price_list[i]}, 현재 가격: {current_price}")

    # 1초 대기
    time.sleep(1)
