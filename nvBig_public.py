from os import link
import sys
import urllib.request
import datetime
import time
import json

client_id = '' #네이버에서 개발자 코드 (아이디, 비번) 받아오세요
client_secret = '' #네이버에서 개발자 코드 (아이디, 비번) 받아오세요

#[CODE 1] url 접속을 요청하고 응답 받아서 반환
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id",client_id)
    req.add_header("X-Naver-Client-Secret",client_secret)
    
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(),url))
        return None
    
    
#[CODE 2] 반환받은 응답 데이터를 파이썬 json 형식으로 반환
def getNaverSearch(node,srcText,start,display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)
    
    url = base + node + parameters
    responseDecode = getRequestUrl(url)
    
    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)
    

#[CODE 3] json 응답 데이터를 정리하여 딕셔너리 리스트인 jsonResult를 구성하고 반환
def getPostData(post, jsonResult, cnt):
    title = post['title']
    link = post['link']   
    jsonResult.append({'title':title, 'link':link})    
    return
"""
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    
    jsonResult.append({'cnt':cnt, 'title':title, 'description':description, 'org_link':org_link, 'link':org_link, 'pDate':pDate})
    return
"""

#[CODE 0]
def main():
    node = input('주제를 입력하세요(news, blog, cafearticle, shop): ')
    srcText = input('검색어를 입력하세요 ')
    cnt = 0
    jsonResult = []
    
    jsonResponse = getNaverSearch(node,srcText,1,100)
    total = jsonResponse['total']
    
    while ((jsonResponse != None) and (jsonResponse['display']!=0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post,jsonResult,cnt)
            
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node,srcText,start,100)
        
    print('전체 검색: %d 건' %total)
    
    with open('%s_naver_%s.json' % (srcText,node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,indent=4,sort_keys=True,ensure_ascii=False)
        
        outfile.write(jsonFile)
        
        print('가져온 데이터 : %d 건' %(cnt))
        print('다음의 이름으로 저장됩니다. ','%s_naver_%s.json SAVED' % (srcText,node))
        
if __name__ == '__main__':
    main()