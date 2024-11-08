#########################################################################
import time
import json
import KIS_Common as Common
import os
import KIS_API_Helper_KR as KisKR

Common.SetChangeMode("VIRTUAL")

save_dir = "/home/agh/stock_bot"
date_kr = Common.GetNowDateStr("KR", "NONE")
print("########################################################")
print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")

MyStockList = KisKR.GetMyStockList()

#def MakeSellLimitOrder(stockcode, amt, price, ErrLog="YES"):

# stock_code_list 불러오는 JSON 파일 경로
source_json_filename = f"sell_stock_code_{date_kr}.json"
source_json_path = os.path.join(save_dir, source_json_filename)

# JSON 파일에서 stock_code_list 불러오기
stock_code_list = []
try:
    with open(source_json_path, "r", encoding="utf-8") as json_file:
        stock_code_list = json.load(json_file)
    print(f"{source_json_filename} 파일에서 종목 코드를 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"{source_json_filename} 파일이 존재하지 않습니다. 빈 리스트로 진행합니다.")

time.sleep(0.5)

for stock_code in stock_code_list:
    try:
        print("시간 : ", time.strftime('%x %X'))
        stock_amt = next((stock['StockAmt'] for stock in MyStockList if stock['StockCode'] == stock_code), None)
        time.sleep(0.5)
        df = Common.GetOhlcv("KR", stock_code, 2)
        start_price = df['open'].iloc[-1]  # 시가
        time.sleep(0.5)
        KisKR.MakeSellLimitOrder(stock_code, stock_amt, start_price, ErrLog="YES")
        print(stock_code)
        print("stock_amt",stock_amt)
        print("start_price", start_price)
        time.sleep(0.5)
    except ValueError:
        print("시간 : ", time.strftime('%x %X'))
        print(f"잘못된 코드: {[stock_code]}")
















