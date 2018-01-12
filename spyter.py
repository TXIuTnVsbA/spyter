# -*- coding: utf-8 -*-
import requests,os,urlparse
from lxml import etree
import threading
import random
requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
#随机数
def random_x(num):
    #seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(num):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return str(salt)

#下载函数
def download(url,log):
    if log==True:
        print url
    tmp=urlparse.urlparse(url)  #read url
    #tmp_scheme = tmp.scheme
    #tmp_netloc = tmp.netloc
    tmp_path = tmp.path #out path:/1/2/3/4/5.test
    tmp_path_split=tmp_path.split("/")  #out path:['',1,2,3,4,5.test]
    tmp_path_tmp=tmp_path_split[1:-1]   #out path:[1,2,3,4]
    tmp_path_len=len(tmp_path_tmp)  #out len:4
    tmp_path_final=tmp_path_split[-1]   #out path:5.test
    for x in range(tmp_path_len):   #双for循环:    1-1;   2-12;   3-123;  4-1234;
        tmp=""
        for y in range(x+1):
            tmp = tmp + tmp_path_tmp[y]+"/"
        if os.path.exists(tmp) == False:
            os.mkdir(tmp)
        if x == tmp_path_len-1:#循环到最后，开始下载并写入文件，返回文件名
            if tmp_path_split[-1]:
                download_ex(url, tmp+tmp_path_final)
                return tmp+tmp_path_final
            else:
                download_ex(url, tmp + tmp+random_x(8))
                return tmp + tmp+random_x(8)

def download_ex(url,file):
    if os.path.exists(file) == False:
        fp = open(file, 'wb')
        fp.write(session.get(url).content)
        fp.close()

def open_text(file):
    file_context=""
    fp = open(file)
    try:
        file_context = fp.read()
    finally:
        fp.close()
    return file_context

#直接解读html
def xpath(url,xp_context):
    try:
        html = str(session.get(url).content)
        selector = etree.HTML(html)
        return selector.xpath(xp_context)
    except:
        return 0

#下载保存后解读html
# 有缺陷，比如http://xxx.com/a/b/?123
# 不知道怎么解决
def xpath_download(url,xp_context):
    try:
        tmp_filename = download(url)
        tmp_file = open_text(tmp_filename)
        selector = etree.HTML(tmp_file)
        return selector.xpath(xp_context)
    except:
        return 0

#根据列表，多线程运行
def list_thread(list,max = 16,target=None):
    #多线程
    i = 0
    result = []
    for tmp in list:
        i = i + 1
        try:
            #print tmp
            T = threading.Thread(target=target, args=(tmp,))
            T.start()
            result.append(T)
        except:
            pass
        if i % max == 0:
            for tmp in result:
                tmp.join()
            del result[:]
    if result:
        for tmp in result:
            tmp.join()
        del result[:]
