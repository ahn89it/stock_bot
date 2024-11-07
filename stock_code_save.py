import final_cal
import ticker_crawling
import index_cal
import json
import KIS_Common as Common
import os

#
# kospi_tickers = ['005945', '075580', '383220', '045100']
# kosdaq_tickers = ['005945', '075580', '383220', '045100']
#
# kospi_change ='상승'
# kosdaq_change ='하락'
save_dir = "/home/agh/stock_bot"


date_kr = Common.GetNowDateStr("KR", "NONE")
print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")

#코스피, 코스닥 지수 상승or하락 확인
kospi_change, kosdaq_change = index_cal.index_cal()
if (kospi_change!='상승' and kosdaq_change!='상승'):
    print("금일 해당 종목 없습니다.")
    # 빈 리스트를 JSON 파일로 저장
    json_filename = f"target_stock_code_{date_kr}.json"
    save_path = os.path.join(save_dir, json_filename)

    # 빈 리스트를 저장합니다.
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump([], json_file, ensure_ascii=False, indent=4)

else:
    #코스피/코스닥 종목코드 수집
    kospi_tickers, kosdaq_tickers = ticker_crawling.ticker_crawling()
    if kospi_change =='상승' and kosdaq_change !='상승':
        result, errors = final_cal.final_cal(kospi_tickers)
    elif kospi_change !='상승' and kosdaq_change =='상승':
        result, errors = final_cal.final_cal(kosdaq_tickers)
    elif kospi_change =='상승' and kosdaq_change =='상승':
        result_tickers = kospi_tickers + kosdaq_tickers
        result, errors = final_cal.final_cal(result_tickers)

    # result를 JSON 파일로 저장하는 부분 추가
    # JSON 파일 이름을 date_kr_none 값으로 설정하여 저장

    json_filename = f"target_stock_code_{date_kr}.json"
    save_path = os.path.join(save_dir, json_filename)

    # 결과를 저장합니다.
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    print(f"결과가 {json_filename} 파일에 저장되었습니다.")

#########################################################################
# test
#
# kospi_tickers = ['005945', '075580', '383220', '045100']
# kosdaq_tickers = ['005945', '075580', '383220', '045100']
#
# kospi_change ='상승'
# kosdaq_change ='하락'
#
#
# date_kr = Common.GetNowDateStr("KR", "NONE")
# print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")
#
# #코스피, 코스닥 지수 상승or하락 확인
#
# if (kospi_change!='상승' and kosdaq_change!='상승'):
#     print("금일 해당 종목 없습니다.")
#     # 빈 리스트를 JSON 파일로 저장
#     json_filename = f"target_stock_code_{date_kr}.json"
#     with open(json_filename, "w", encoding="utf-8") as json_file:
#         json.dump([], json_file, ensure_ascii=False, indent=4)
#
#
# else:
#     #코스피/코스닥 종목코드 수집
#     #kospi_tickers, kosdaq_tickers = ticker_crawling.ticker_crawling()
#     if kospi_change =='상승' and kosdaq_change !='상승':
#         result, errors = final_cal.final_cal(kospi_tickers)
#     elif kospi_change !='상승' and kosdaq_change =='상승':
#         result, errors = final_cal.final_cal(kosdaq_tickers)
#     elif kospi_change =='상승' and kosdaq_change =='상승':
#         result_tickers = kospi_tickers + kosdaq_tickers
#         result, errors = final_cal.final_cal(result_tickers)
#
#     # result를 JSON 파일로 저장하는 부분 추가
#     # JSON 파일 이름을 date_kr_none 값으로 설정하여 저장
#     json_filename = f"target_stock_code_{date_kr}.json"
#     result = ['005945', '075580', '383220', '045100']
#     with open(json_filename, "w", encoding="utf-8") as json_file:
#         json.dump(result, json_file, ensure_ascii=False, indent=4)
#
#     print(f"결과가 {json_filename} 파일에 저장되었습니다.")