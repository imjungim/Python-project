from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import csv

#브라우저생성
browser = webdriver.Chrome('D:\python\chromedriver.exe')
#웹사이트 열기
browser.get('https://www.naver.com')
browser.implicitly_wait(10) #로딩이 끝날 때까지 10초 기다려줌
#쇼핑메뉴 클릭
browser.find_element_by_css_selector('a.nav.shop').click()
time.sleep(2)
#검색창 클릭
search=browser.find_element_by_css_selector('input.co_srh_input._input')
search.click()

#검색어 입력
search.send_keys('이북리더기')
search.send_keys(Keys.ENTER) 

#csv파일로 저장(파일생성)
f=open(r"D:\python\data.csv",'w',encoding='CP949',newline='')
#경로,쓰기모드,인코딩,줄바꿈없애기
csvWriter = csv.writer(f)


for i in range(1,6):  
  before_h = browser.execute_script("return window.scrollY")  # execute_script 자바스크립트 명령어
  #스크롤을 내리기 전 높이를 확인 (자바스크립트의 명령어 수행 현재 스크롤된 위치를 계산해서 저장)현재 스크롤된 높이를 계산 처음에는0
  
  # 무한 스크롤 (반복문)
  while True:
    
    browser.find_element_by_css_selector('body').send_keys(Keys.END) #키보드의 End키를 이용해 스크롤을 아래로 내림
    
    time.sleep(1) #(페이지 로딩시간추가)
    
    #스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")
    
    if after_h == before_h: #스크롤 전과 스크롤 후의 높이가 같아지면
      break
    before_h = after_h  
  #상품정보 가져오기(리스트형태) -> for문으로 뽑아주기
  items = browser.find_elements_by_css_selector('.basicList_info_area__17Xyo')
    
  for item in items:
    name = item.find_element_by_css_selector('.basicList_title__3P9Q7').text #상품이름
      
    #예외처리
    try :
      price = item.find_element_by_css_selector('.price_num__2WUXn').text #상품가격
    except:
      price = "판매중단"
        
    link = item.find_element_by_css_selector('.basicList_title__3P9Q7 > a').get_attribute('href')
    print(name, price, link)
    
      #데이터쓰기
    csvWriter.writerow([name,price,link])
    #다음 페이지 버튼 클릭
  browser.find_element_by_css_selector('.pagination_next__1ITTf').click()
      
f.close()
