from bs4 import BeautifulSoup
import re
import requests as rq
from io import BytesIO
import pandas as pd
import numpy as np

def ticker_crawling():
    # 네이버 금융 사이트에서 기준일 수집
    url = 'https://finance.naver.com/sise/sise_deposit.nhn'
    data = rq.get(url)
    data_html = BeautifulSoup(data.content, 'html.parser')
    parse_day = data_html.select_one('div.subtop_sise_graph2 > ul.subtop_chart_note > li > span.tah').text
    biz_day = re.findall('[0-9]+', parse_day)
    biz_day = ''.join(biz_day)
    print("네이버증권 기준일 티커 수집", biz_day)

    # OTP 생성 및 데이터 수집
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    gen_otp_stk = {
        'mktId': 'STK',
        'trdDd': biz_day,
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
    }

    headers = {
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'connection': 'keep-alive',
        'content-length': '133',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__smVisitorID=D2spgRf7-CX; JSESSIONID=H6Xb8DmFOdEgcHrtuNsNVuHWbo0NeCMf1YjRHSvXcp7makjTz2ycVJVHP03oVGdJ.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==',
        'host': 'data.krx.co.kr',
        'origin': 'http://data.krx.co.kr',
        'referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers=headers).text
    #print(otp_stk)

    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    down_sector_stk = rq.post(down_url, {'code': otp_stk}, headers=headers)
    sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

    # 코스닥 데이터 수집
    gen_otp_ksq = {
        'mktId': 'KSQ',  # 코스닥 입력
        'trdDd': biz_day,
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
    }
    otp_ksq = rq.post(gen_otp_url, gen_otp_ksq, headers=headers).text
    #print(otp_ksq)

    down_sector_ksq = rq.post(down_url, {'code': otp_ksq}, headers=headers)
    sector_ksq = pd.read_csv(BytesIO(down_sector_ksq.content), encoding='EUC-KR')

    # KRX 섹터 통합
    krx_sector = pd.concat([sector_stk, sector_ksq]).reset_index(drop=True)
    krx_sector['종목명'] = krx_sector['종목명'].str.strip()
    krx_sector['기준일'] = biz_day

    # 종목 기본 데이터 수집
    gen_otp_data = {
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': biz_day,
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03501'
    }

    otp = rq.post(gen_otp_url, gen_otp_data, headers=headers).text
    #print(otp)

    krx_ind = rq.post(down_url, {'code': otp}, headers=headers)
    krx_ind = pd.read_csv(BytesIO(krx_ind.content), encoding='EUC-KR')
    krx_ind['종목명'] = krx_ind['종목명'].str.strip()
    krx_ind['기준일'] = biz_day

    # 데이터 병합 및 클렌징
    diff = list(set(krx_sector['종목명']).symmetric_difference(set(krx_ind['종목명'])))
    kor_ticker = pd.merge(
        krx_sector,
        krx_ind,
        on=krx_sector.columns.intersection(krx_ind.columns).tolist(),
        how='outer'
    )

    kor_ticker['종목구분'] = np.where(
        kor_ticker['종목명'].str.contains('스팩|제[0-9]+호'), '스팩',
        np.where(
            kor_ticker['종목코드'].str[-1:] != '0', '우선주',
            np.where(
                kor_ticker['종목명'].str.endswith('리츠'), '리츠',
                np.where(kor_ticker['종목명'].isin(diff), '기타', '보통주')
            )
        )
    )

    kor_ticker = kor_ticker.reset_index(drop=True)
    kor_ticker.columns = kor_ticker.columns.str.replace(' ', '')
    kor_ticker = kor_ticker[['종목코드', '종목명', '시장구분', '기준일', '종목구분']]
    kor_ticker = kor_ticker.replace({np.nan: None})
    kor_ticker['기준일'] = pd.to_datetime(kor_ticker['기준일'])

    # KOSPI와 KOSDAQ 종목코드 리스트 생성
    kospi_ticker_list = kor_ticker[kor_ticker['시장구분'] == 'KOSPI']['종목코드'].tolist()
    kosdaq_ticker_list = kor_ticker[kor_ticker['시장구분'] == 'KOSDAQ']['종목코드'].tolist()

    # 결과 출력
    print(f"KOSPI 개수: {len(kospi_ticker_list)}")
    print(f"KOSDAQ 개수: {len(kosdaq_ticker_list)}")
    print(f"KOSPI 종목코드 리스트: {kospi_ticker_list}")
    print(f"KOSDAQ 종목코드 리스트: {kosdaq_ticker_list}")

    return kospi_ticker_list, kosdaq_ticker_list


