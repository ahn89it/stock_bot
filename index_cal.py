import requests
from bs4 import BeautifulSoup



def index_cal():
    # 목표 URL
    url = "https://finance.naver.com/"

    # HTTP 요청 헤더 설정 (User-Agent를 설정하여 브라우저에서 요청하는 것처럼 보이게 함)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 웹 페이지 요청
    response = requests.get(url, headers=headers)

    # HTTP 요청이 성공적으로 완료되었는지 확인
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # kospi_area group_quot quot_opn 클래스 선택
        kospi_area_div = soup.find('div', class_='kospi_area group_quot quot_opn')
        kosdaq_area_div = soup.find('div', class_='kosdaq_area group_quot')

        heading_area_div = kospi_area_div.find('div', class_='heading_area')
        heading_area_div2 = kosdaq_area_div.find('div', class_='heading_area')
        text_content = heading_area_div.get_text(strip=True)
        text_content2 = heading_area_div2.get_text(strip=True)
        kospi_index = text_content[-2:]
        kosdaq_index = text_content2[-2:]
        print(f"코스피 지수 : {kospi_index}")
        print(f"코스닥 지수 : {kosdaq_index}")
        return kospi_index, kosdaq_index
    else:
        print("err: 지수 등락률 읽기 실패")
        return None, None




