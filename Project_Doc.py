

"""

======================================================================================
*매수 프로세스
순서
(1) token_save.py  (00시 01분 1회 실행)
(2) stock_code_save.py (00시 05분 1회 실행)
(3) target_stock_info_save.py (09시 01분 1회 실행)
(4) buy_stock2.py (09시03분 - 매1초 마다 실행)
======================================================================================
매도
sell_stock.py





(1) token_save.py
-토큰값 파일저장 (stock_token_real.jsaon / stock_token_virtual.json)
-크론탭은 00시 넘어서
-※토큰 : 증권사에서 매일 토큰을 제공하여 접근을 가능하게 한다. 매일 1회 발급

(2) stock_code_save.py
- 코스피/코스닥 지수 상승/하락 판별 -> 목표 종목 리스트 선정 -> 종목리스트 파일 저장
- import(index_cal.py, final_cal.py)
- index_cal.py : 코스피/코스닥 지수 상승/하락 판별
- final_cal.py : 조건에 맞는 종목 선별하는 알고리즘 수식
- stock_code_save.py : 코스파/코스닥 지수 상승시 final_cal.py 실행 후 종목 리스트 저장(json으로 저장)
                       (코스피/코스닥 지수 모두 상승시 대략 2시간~2시간 반 소요) ,
                      코스피/코스닥 지수 모두 하락시 최종 빈 리스트로 저장
- json으로 저장되는 파일제목 : target_stock_code_{date_kr}.json

(3) target_stock_info_save.py
- (2)stock_code_save.py에서 저장된 json파일을 읽어서 list('stock_code_list')로 저장
- stock_code_list의 종목들을 읽어서 코스피/코스닥 시장 확인 후 목표가 설정
- df = Common.GetOhlcv로 당일시가, 전날고가, 전날저가 불러오기
- 목표가는 #호가 단위에 맞게 가격 조정 ( adjust_target_price = KisKR.PriceAdjust 함수 사용)
- 목표가를 리스트로 저장
- DantaDataList 로 dic 형태로 저장
  'stock_code': stock_code_list[i],
   'buy_check': "False",   매수주문 전 : False, 매수주문 후: True
  'target_price': target_price_list[i]
- Dic 형태로 target_stock_info_{date_kr}.json" 이름으로 최종 저장



(4) buy_stock2.py
-
실시간 현재가 - 목표가 일치한지 확인 -> 일치하면 목표가로 매수 주문



*매도 프로세스
sell_stock
(1) 매도할 주식 종목들 : sell_stock_code_{date_kr}.json 파일을 읽어서  stock_code_list 에 저장
(2) 시장가로 매도 주문

"""