# python2
# coding = utf-8
import io,shutil
import codecs
import sys
import os
import datetime
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

def read_file_content_en(filename, encoding = 'utf8', ignore_empty = True):
    result_list = []
    fr = codecs.open(filename, 'r', encoding)
    index = 0;
    #print ('filename= ', filename)
    for text in fr:
        index += 1
        text = text.strip('\n')
        text = text.strip()
        if len(text) > 0 and text[0] != '#':
            result_list.append(text)
        elif not ignore_empty:
            result_list.append(text)
    return result_list


tmp_list = read_file_content_en('mysql_config2')
#tmp_list = [e for e in tmp_list if e.find('select_dtu3_') != -1 ]
res = {}
for e in tmp_list:
    tmp = e.split('|')[1:3]
    if len(tmp) >= 2:
        try:
            res[tmp[0].strip()] = json.loads(tmp[1])
        except:
            res[tmp[0].strip()] = {tmp[0].strip():tmp[1].strip()}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        path = self.path
        print path
        key = path.split('/')[1]
        response = {
            'error': 'not find key:' + key
        }
        if key in res:
            response = res[key]
        else:
            for k,v in res.items():
                print '|||%s|||'%k, len(k)

        self._set_headers()
        self.wfile.write(json.dumps(response))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print 'post data from client:'
        print post_data

        response = {
            'status':'SUCCESS',
            'data':'server got your post data'
        }
        self._set_headers()
        self.wfile.write(json.dumps(response))

def run():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

run()

