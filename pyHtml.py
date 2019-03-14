#!/usr/bin/python
#-*- coding: gb18030 -*-

import sys
import urllib
import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar
import socket,gzip

import pyIO

def installProxyHandle(isWebPorxy = True, isHKProxy = False, isTencentProxy = False):
    
    proxy_handler = None
    if isWebPorxy:
        proxy_handler = urllib.request.ProxyHandler({"http" : 'http://web-proxy.oa.com:8080'})
    if isHKProxy:
        proxy_handler = urllib.request.ProxyHandler({"http" : 'http://web-proxyhk.oa.com:8080'})
    if isTencentProxy:
        proxy_handler = urllib.request.ProxyHandler({"http" : 'http://proxy.tencent.com:8080'})
    
    if proxy_handler is not None:
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    else:
        logging.info('no proxy set!')

###获取HTML文本数据
def getHtmlData(total_url, isUsingUrllib2 = True):
    if not isUsingUrllib2:
        url_link, url_req = splitGoogleUrlAndRequest(total_url)
        conn = httplib.HTTPConnection(url_link)
        conn.request("GET", url_req)
        r1 = conn.getresponse()
        ##200 OK
        if 200 == r1.status:
            data = r1.read()
            logging.info('data len= %d'%len(data))
            #conn.close()
            return data, True
        else:
            #print r1.status, r1.reason
            logging.info('r1= %d'%r1)
            return r1.url, False
    else:
        i_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
             
        #print 'total_url= ', total_url
        req = urllib.request.Request(total_url, headers=i_headers)
        response = urllib.request.urlopen(req, timeout = 10)
        the_page = response.read()
        return the_page


class HttpTester:
    def __init__(self, timeout=10, addHeaders=True):
        socket.setdefaulttimeout(timeout)   # 设置超时时间
 
        self.__opener = urllib.request.build_opener()
        urllib.request.install_opener(self.__opener)
 
        if addHeaders: self.__addHeaders()
 
    def __error(self, e):
        '''错误处理'''
        print(e)
 
    def __addHeaders(self):
        '''添加默认的 headers.'''
        self.__opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'),
                                    ('Connection', 'keep-alive'),
                                    ('Cache-Control', 'no-cache'),
                                    ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                                    ('Accept-Encoding', 'gzip, deflate'),
                                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
 
    def __decode(self, webPage, charset):
        '''gzip解压，并根据指定的编码解码网页'''
        if webPage.startswith(b'\x1f\x8b'):
            return gzip.decompress(webPage).decode(charset)
        else:
            return tryDecode(webPage)
            #return webPage.decode(charset)
 
    def addCookiejar(self):
        '''为 self.__opener 添加 cookiejar handler。'''
        cj = http.cookiejar.CookieJar()
        self.__opener.add_handler(urllib.request.HTTPCookieProcessor(cj))
 
    def addProxy(self, host, type='http'):
        '''设置代理'''
        proxy = urllib.request.ProxyHandler({type: host})
        self.__opener.add_handler(proxy)
 
    def addAuth(self, url, user, pwd):
        '''添加认证'''
        pwdMsg = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pwdMsg.add_password(None, url, user, pwd)
        auth = urllib.request.HTTPBasicAuthHandler(pwdMsg)
        self.__opener.add_handler(auth)
 
    def get(self, url, params={}, headers={}, charset='UTF-8'):
        '''HTTP GET 方法'''
        if params: url += '?' + urllib.parse.urlencode(params)
        
#         print('params= ', params['q'], 'url= ', url)
#         sys.exit(0)
        
        request = urllib.request.Request(url)
        for k,v in headers.items(): request.add_header(k, v)    # 为特定的 request 添加指定的 headers
 
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset)
            #return pyIO.tryDecode(response.read())
 
    def post(self, url, params={}, headers={}, charset='UTF-8'):
        '''HTTP POST 方法'''
        
        params = urllib.parse.urlencode(params)
        d = params.encode(charset)
#         print(get_cur_info(), 'd= ', d, charset)
        request = urllib.request.Request(url, data=d)  # 带 data 参数的 request 被认为是 POST 方法。
        
        for k,v in headers.items(): request.add_header(k, v)
        
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset)
 
    def download(self, url, savefile):
        '''下载文件或网页'''
        header_gzip = None
 
        for header in self.__opener.addheaders:     # 移除支持 gzip 压缩的 header
            if 'Accept-Encoding' in header:
                header_gzip = header
                self.__opener.addheaders.remove(header)
 
        __perLen = 0
        def reporthook(a, b, c):    # a:已经下载的数据大小; b:数据大小; c:远程文件大小;
            if c > 1000000:
                #nonlocal __perLen
                per = (100.0 * a * b) / c
                if per>100: per=100
                per = '{:.2f}%'.format(per)
                __perLen = len(per)+1
                ###### print('\b'*__perLen, per, end='')     # 打印下载进度百分比
                print('\b'*__perLen, per)
                sys.stdout.flush()
                #__perLen = len(per)+1
 
        ###### print('--> {}\t'.format(url), end='')
        try:
            urllib.request.urlretrieve(url, savefile, reporthook)   # reporthook 为回调钩子函数，用于显示下载进度
        except urllib.error.HTTPError as e:
            self.__error(e)
        finally:
            self.__opener.addheaders.append(header_gzip)
            print()

#     def extract_url_and_content2(self, url_prefix, data):
#         #print get_cur_info(), '......'
#         
#         soup = BeautifulSoup(data.lower())
#         url_dict = {}
#         tag = soup.findAll('a', {'href':True})
#         #print get_cur_info(), 'a tag len= ', len(tag)
#         
#         for e in tag:
#             url = dict(e.attrs)['href']
#             url = self.format_url(url_prefix, url)
#             url_dict[url] = True
#             
#         content_dict = {}
# #         tag = soup.findAll('font')
# #         print get_cur_info(), 'tag len= ', len(tag)
# #         for e in tag:
# #             content_dict[e.string] = True
# #             print get_cur_info(), 'tag len= ', len(tag), e.string
# 
#         tag = soup.findAll('p')
#         #print get_cur_info(), 'p tag len= ', len(tag)
#         for e in tag:
#             content_dict[e.string] = True
#             #print get_cur_info(), 'p tag len= ', len(tag), e.string
# 
#         tag = soup.findAll('span')
#         #print get_cur_info(), 'span tag len= ', len(tag)
#         for e in tag:
#             content_dict[e.string] = True
# 
#         tag = soup.findAll('div')
#         #print get_cur_info(), 'div tag len= ', len(tag)
#         for e in tag:
#             content_dict[e.string] = True
#             #print get_cur_info(), 'span tag len= ', len(tag), e.string
#         
#         return url_dict, content_dict
