# -*- coding: utf-8 -*-
import sys, hashlib, os, random, urllib, urllib2
from datetime import *

class APIClient(object):
    def http_request(self, url, paramDict):
        post_content = ''
        for key in paramDict:
            post_content = post_content + '%s=%s&'%(key,paramDict[key])
        post_content = post_content[0:-1]
        #print post_content
        req = urllib2.Request(url, data=post_content)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, post_content)  
        return response.read()

    def http_upload_image(self, url, paramKeys, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n'%(boundary)
        
        bs = b''
        for key in paramKeys:
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, paramDict[key])
            #print param
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')
        
        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n'%('sample')
        bs = bs + header.encode('utf8')
        
        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n'%(boundary)
        bs = bs + tailer.encode('ascii')
        
        import requests
        headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
                   'Connection':'Keep-Alive',
                   'Expect':'100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)
        return response.text

def arguments_to_dict(args):
    argDict = {}
    if args is None:
        return argDict
    
    count = len(args)
    if count <= 1:
        print 'exit:need arguments.'
        return argDict
    
    for i in [1,count-1]:
        pair = args[i].split('=')
        if len(pair) < 2:
            continue
        else:
            argDict[pair[0]] = pair[1]

    return argDict

def get_captcha(image_url):
    client = APIClient()
    while 1:
        paramDict = {}
        result = ''
        act = raw_input('请输入打码方式url:')
        if cmp(act, 'info') == 0: 
            paramDict['username'] = raw_input('username:')
            paramDict['password'] = raw_input('password:')
            result = client.http_request('http://api.ruokuai.com/info.xml', paramDict)
        elif cmp(act, 'register') == 0:
            paramDict['username'] = raw_input('username:')
            paramDict['password'] = raw_input('password:')
            paramDict['email'] = raw_input('email:')
            result = client.http_request('http://api.ruokuai.com/register.xml', paramDict)
        elif cmp(act, 'recharge') == 0:
            paramDict['username'] = raw_input('username:')
            paramDict['id'] = raw_input('id:')
            paramDict['password'] = raw_input('password:')
            result = client.http_request('http://api.ruokuai.com/recharge.xml', paramDict)
        elif cmp(act, 'url') == 0:
            paramDict['username'] = '********'
            paramDict['password'] = '********'
            paramDict['typeid'] = '2000'
            paramDict['timeout'] = '90'
            paramDict['softid'] = '76693'
            paramDict['softkey'] = 'ec2b5b2a576840619bc885a47a025ef6'
            paramDict['imageurl'] = image_url
            result = client.http_request('http://api.ruokuai.com/create.xml', paramDict)
        elif cmp(act, 'report') == 0:
            paramDict['username'] = raw_input('username:')
            paramDict['password'] = raw_input('password:')
            paramDict['id'] = raw_input('id:')
            result = client.http_request('http://api.ruokuai.com/create.xml', paramDict)
        elif cmp(act, 'upload') == 0:
            paramDict['username'] = '********'
            paramDict['password'] = '********'
            paramDict['typeid'] = '2000'
            paramDict['timeout'] = '90'
            paramDict['softid'] = '76693'
            paramDict['softkey'] = 'ec2b5b2a576840619bc885a47a025ef6'
            paramKeys = ['username',
                 'password',
                 'typeid',
                 'timeout',
                 'softid',
                 'softkey'
                ]

            from PIL import Image
            imagePath = raw_input('Image Path:')
            img = Image.open(imagePath)
            if img is None:
                print 'get file error!'
                continue
            img.save("upload.gif", format="gif")
            filebytes = open("upload.gif", "rb").read()
            result = client.http_upload_image("http://api.ruokuai.com/create.xml", paramKeys, paramDict, filebytes)
        
        elif cmp(act, 'help') == 0:
            print 'info'
            print 'register'
            print 'recharge'
            print 'url'
            print 'report'
            print 'upload'
            print 'help'
            print 'exit'
        elif cmp(act, 'exit') == 0:
            break
        
        return result