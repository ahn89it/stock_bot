'''

하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

주식/코인 자동매매 FAQ
https://blog.naver.com/zacra/223203988739

그래도 안 된다면 구글링 해보시고
그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

클래스 제작 완료 후 많은 시간이 흘렀고 그 사이 전략에 많은 발전이 있었습니다.
제가 직접 투자하고자 백테스팅으로 검증하여 더 안심하고 있는 자동매매 전략들을 블로그에 공개하고 있으니
완강 후 꼭 블로그&유튜브 심화 과정에 참여해 보세요! 기다릴께요!!

아래 빠른 자동매매 가이드 시간날 때 완독하시면 방향이 잡히실 거예요!
https://blog.naver.com/zacra/223086628069


'''
import KIS_Common as Common
import KIS_API_Helper_KR as KisKR
import json
import os
import time
Common.SetChangeMode("VIRTUAL")


date_kr = Common.GetNowDateStr("KR", "NONE")
print("########################################################")
#print(f"한국 현재 날짜 (YYYYMMDD): {date_kr}")


save_dir = "/home/agh/stock_bot"
# 종목 정보 담긴 JSON 파일 이름
json_filename = f"target_stock_info_{date_kr}.json"
save_path = os.path.join(save_dir, json_filename)

TargetMoney =200000
#print("각 종목당 투자할 금액:",TargetMoney)



# 종목 코드가 담긴 JSON 파일 이름
input_json_filename = os.path.join(save_dir, json_filename)

with open(input_json_filename, "r", encoding="utf-8") as json_file:
    DantaDataList = json.load(json_file)



for Data in DantaDataList:
    current_price = KisKR.GetCurrentPrice(Data['stock_code'])
    time.sleep(1)
    try:
        if (Data['buy_check']) == "False" and (current_price >= Data['target_price']):
            time.sleep(1)
            amt = TargetMoney / float(current_price)
            KisKR.MakeBuyLimitOrder(Data['stock_code'], amt, Data['target_price'], True, "NO")
            time.sleep(1)
            Data['buy_check'] = "True"
            print("=============================================================")
            print("시간 : ", time.strftime('%x %X'))
            print(f"종목 코드: {Data['stock_code']}, 현재 가격: {current_price}, 목표가격: {Data['target_price']}")
            print(f"check point: {Data['buy_check']}")
            print("=============================================================")
            time.sleep(1)
    except ValueError:
        print("시간 : ", time.strftime('%x %X'))
        print(f"잘못된 코드: {Data['stock_code']}")




with open(save_path, "w", encoding="utf-8") as json_file:
    json.dump(DantaDataList, json_file, ensure_ascii=False, indent=4)


