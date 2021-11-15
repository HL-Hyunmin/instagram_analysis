from _typeshed import WriteableBuffer
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import openpyxl
import pandas as pd
import numpy as np 
#함수 정의 검색어 조건 url 생성

def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/'+str(word)
    return url 


# 게시물 클릭 함 수 정의 
def select_first(driver):
    first = driver.find_elements_by_css_selector('div._9AhH0')[0]
    first.click()
    time.sleep(4)

#게시물 본문 날자 좋아요 위치 정보 해시태그 갖고오기

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    #content 내용
    try: 
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    #해시 태그
    tags = re.findall(r'#[^\s#,\\]+', content)
    #작성일자 
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    #좋아요 
    try: 
        like = soup.select('div.Nm9Fw a span')[0].text
    except:
        like = 0 
    #위치 
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ' '
    data = [content, date, like, place, tags]
    return data 

# 함수 정의 : 개시물 클릭 후 다음 게시물로 이동 
def move_next(driver):
    right = driver.find_element_by_css_selector('a.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(np.random.uniform(4,11))

# 크롬 시작 
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.instagram.com')
time.sleep(4)

#인스타그램 로그인 
email = 'gp1091@daum.net'
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = 'Qawsedrft5%'
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(5)

#게시물 조회할 검색어 
word = input('검색어 : ')

word = str(word)
url = insta_searching(word)

# 검색 결과 페이지 열기 
driver.get(url)
time.sleep(np.random.uniform(3,8))

#첫 번째 게시물 클릭 
select_first(driver)

# 데이터 수집 시작 
resu = []
target = 900

for i in range(target):

    try:
        data = get_content(driver)
        resu.append(data)
        move_next(driver)
    except:
        time.sleep(np.random.uniform(3,11))
        move_next(driver)
    
print(resu)



#, columns=['content','date','like','place','tags'])
res_df = pd.DataFrame(resu)
res_df.columns = ['content', 'date', 'like', 'place', 'tags']
res_df.to_excel('Hot.xlsx')

