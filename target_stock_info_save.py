# import time
# import final_cal
# import ticker_crawling
# import index_cal
# import json
# import KIS_Common as Common
# import os
# import market_search
# import KIS_API_Helper_KR as KisKR
# Common.SetChangeMode("VIRTUAL")
# #
# # kospi_tickers = ['005945', '075580', '383220', '045100']
# # kosdaq_tickers = ['005945', '075580', '383220', '045100']
# #
# # kospi_change ='상승'
# # kosdaq_change ='하락'
# save_dir = "/home/agh/stock_bot"
# date_kr = Common.GetNowDateStr("KR", "NONE")
# print("########################################################")
# print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")
#
# # 종목 정보 담긴 JSON 파일 이름
# json_filename = f"target_stock_info_{date_kr}.json"
# save_path = os.path.join(save_dir, json_filename)
#
#
# #코스피, 코스닥 지수 상승or하락 확인
# kospi_change, kosdaq_change = index_cal.index_cal()
# if (kospi_change!='상승' and kosdaq_change!='상승'):
#     print("금일 해당 종목 없습니다.")
#     # 빈 리스트를 JSON 파일로 저장
#     # 빈 리스트를 저장합니다.
#
#     with open(save_path, "w", encoding="utf-8") as json_file:
#         json.dump([], json_file, ensure_ascii=False, indent=4)
#
# else:
#     #코스피/코스닥 종목코드 수집
#     kospi_tickers, kosdaq_tickers = ticker_crawling.ticker_crawling()
#     if kospi_change =='상승' and kosdaq_change !='상승':
#         stock_code_list, errors = final_cal.final_cal(kospi_tickers)
#     elif kospi_change !='상승' and kosdaq_change =='상승':
#         stock_code_list, errors = final_cal.final_cal(kosdaq_tickers)
#     elif kospi_change =='상승' and kosdaq_change =='상승':
#         stock_code_list_tickers = kospi_tickers + kosdaq_tickers
#         stock_code_list, errors = final_cal.final_cal(stock_code_list_tickers)
#
#     target_price_list = []
#
#     for stock_code in stock_code_list:
#         if (market_search.get_market_type(stock_code) == 'kospi'):
#             nanugi = 2.5
#         else:
#             nanugi = 2
#         # GetOhlcv 함수에 종목 코드를 넣고 처리 (2일치 데이터를 가져옴)
#         df = Common.GetOhlcv("KR", stock_code, 4)
#         # print(df)
#         start_price = df['open'].iloc[-1]  # 시가
#         high_price = df['high'].iloc[-2]  # 전날 고가
#         low_price = df['low'].iloc[-2]  # 전날 저가
#         target_price = start_price + (high_price - low_price) / nanugi
#         adjust_target_price = KisKR.PriceAdjust(target_price, stock_code)  # 호가 단위에 맞게 target_price 가격 조정!!!!
#         target_price_list.append(adjust_target_price)
#         time.sleep(2)
#
#
#
#
#     # 빈 리스트 생성
#     DantaDataList = []
#
#     # stock_code_list의 길이를 기준으로 for문을 돌림
#     for i in range(len(stock_code_list)):
#         # 각 stock_code와 target_price를 사용하여 딕셔너리를 생성하고 buy_check를 False로 설정
#         data = {
#             'stock_code': stock_code_list[i],
#             'buy_check': "False",
#             'target_price': target_price_list[i]
#         }
#         # 생성된 딕셔너리를 DantaDataList에 추가
#         DantaDataList.append(data)
#
#     # 결과 출력
#     print(DantaDataList)
#
#     # 결과를 저장합니다.
#     with open(save_path, "w", encoding="utf-8") as json_file:
#         json.dump(DantaDataList, json_file, ensure_ascii=False, indent=4)
#
#     print(f"결과가 {json_filename} 파일에 저장되었습니다.")

#########################################################################
import time
import json
import KIS_Common as Common
import os
import market_search
import KIS_API_Helper_KR as KisKR

Common.SetChangeMode("VIRTUAL")

save_dir = "/home/agh/stock_bot"
date_kr = Common.GetNowDateStr("KR", "NONE")
print("########################################################")
print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")

# 최종 파일 저장 정보
json_filename = f"target_stock_info_{date_kr}.json"
save_path = os.path.join(save_dir, json_filename)

# stock_code_list 불러오는 JSON 파일 경로
source_json_filename = f"target_stock_code_{date_kr}.json"
source_json_path = os.path.join(save_dir, source_json_filename)

# JSON 파일에서 stock_code_list 불러오기
stock_code_list = []
try:
    with open(source_json_path, "r", encoding="utf-8") as json_file:
        stock_code_list = json.load(json_file)
    print(f"{source_json_filename} 파일에서 종목 코드를 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"{source_json_filename} 파일이 존재하지 않습니다. 빈 리스트로 진행합니다.")

# 목표 가격 리스트 생성
target_price_list = []

for stock_code in stock_code_list:
    nanugi = 2.5 if market_search.get_market_type(stock_code) == 'kospi' else 2
    df = Common.GetOhlcv("KR", stock_code, 4)
    start_price = df['open'].iloc[-1]
    high_price = df['high'].iloc[-2]
    low_price = df['low'].iloc[-2]
    target_price = start_price + (high_price - low_price) / nanugi
    adjust_target_price = KisKR.PriceAdjust(target_price, stock_code)
    target_price_list.append(adjust_target_price)
    print("start_price", start_price)
    print("high_price", high_price)
    print("low_pricce", low_price)
    print("nanugi", nanugi)
    time.sleep(2)

# 빈 리스트 생성
DantaDataList = []

# stock_code_list의 길이를 기준으로 for문을 돌림
for i in range(len(stock_code_list)):
    data = {
        'stock_code': stock_code_list[i],
        'buy_check': "False",
        'target_price': target_price_list[i]
    }
    DantaDataList.append(data)

    # 결과 출력
print(DantaDataList)

# 결과를 저장합니다.
with open(save_path, "w", encoding="utf-8") as json_file:
    json.dump(DantaDataList, json_file, ensure_ascii=False, indent=4)

print(f"결과가 {json_filename} 파일에 저장되었습니다.")