import requests
from bs4 import BeautifulSoup


def get_market_type(code):
    # 입력받은 code로 URL 생성
    url = f"https://finance.naver.com/item/main.naver?code={code}"

    # 웹 페이지 요청
    response = requests.get(url)

    # 요청 성공 여부 확인
    if response.status_code != 200:
        return "페이지를 불러오지 못했습니다."

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # class 값이 kosdaq 또는 kospi인 img 태그 찾기
    img_element = soup.find('img', class_=['kosdaq', 'kospi'])

    # 결과 반환 (class 값 반환)
    if img_element:
        return img_element['class'][0]  # 'kosdaq' 또는 'kospi' 반환
    else:
        return "요소를 찾을 수 없습니다."


# 사용 예시
# code = input("종목 코드를 입력하세요 (6자리 숫자): ")
# market_type = get_market_type(code)
# print(f"해당 종목은 {market_type}입니다.")
