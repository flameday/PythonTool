#!/usr/local/bin/python3

import http.cookiejar,urllib,sys,time,http,os,sys
from bs4 import BeautifulSoup
import subprocess
from random import randint
from time import sleep
from datetime import datetime

###模拟登录
cj=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
exheaders=[      
    ('Host','passport.tianya.cn'),
    ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'),  
    ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Language','zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
    ('Accept-Encoding','gzip,deflate'),
    ('Referer','http://www.tianya.cn/'),
    ('Connection','keep-alive'),
    ('Content-Type','application/x-www-form-urlencoded')
]
def get_filename(filename):
    dir_password = os.path.dirname(__file__)
    if len(dir_password) > 0:
        dir_password += '/' + filename
    else:
        dir_password = './' + filename
    return dir_password

password = open(get_filename('password.txt'), 'r').read()
opener.addheaders=exheaders
loginurl='https://passport.tianya.cn/login?from=index&_goto=login'
postdate=urllib.parse.urlencode({'vwriter': 'flameday',
                            'vpassword': password,
                          })
re=opener.open(loginurl,postdate.encode('utf-8'))
#print (re.info())

def get_time():
    f = open(get_filename('time.txt'), 'r')
    last_time = f.read()
    f.close()
    return last_time
def write_time(time_val):
    f = open(get_filename('time.txt'), 'w')
    f.write(time_val)
    f.close()

def get_index():
    f = open(get_filename('index.txt'), 'r')
    last_index = f.read()
    f.close()
    return last_index

def write_index(index_val):
    f = open(get_filename('index.txt'), 'w')
    f.write(str(index_val))
    f.close()

index = get_index()
try:
    index = int(index)
except:
    index = 1

for i in range(index, index+30):
    url = 'http://bbs.tianya.cn/post-stocks-1959291-%s.shtml'%i
    print(datetime.now(), 'url:', url)

    sleep(randint(1,5))

    response = urllib.request.urlopen(url)
    dlurl = response.geturl()
    if dlurl != url:
        print('end to url index')
        break

    html = response.read()
    #print (datetime.now(), 'html=', html.decode('utf8'))
    soup = BeautifulSoup(html.decode('utf8'), "lxml")

    ###get time
    last_time = get_time()

    time_list = []
    for div in soup.find_all("div", class_='atl-item'):
        #print('------------------')
        #print(div.name)
        #print(div.attrs['js_username'], div.attrs['js_restime'])
        #print(div.attrs)
        if 'js_username' in div.attrs and div.attrs['js_username'] == '量子之鹰':
            matched = True
            time_list.append(div.attrs['js_restime'])
            try:
                print(datetime.now(), div.attrs['js_username'].encode('utf8'), div.attrs['js_restime'].encode('utf8'))
            except e:
                pass
    print(datetime.now(), 'last_time:', last_time, ' index:', i)
    print(datetime.now(), 'time_list:', time_list)

    if len(time_list) > 0 and time_list[-1] != last_time:
        write_time(time_list[-1])
        write_index(i)
    
        applescript = """
            display dialog "量子之鹰说话了..." ¬
    with title "This is a pop-up window" ¬
    with icon caution ¬
    buttons {"OK"}
        """
        
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
        break
