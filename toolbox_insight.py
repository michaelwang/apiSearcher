#-*- encoding:utf-8-*-
#FileName: toolbox_insight.py
from sgmllib import SGMLParser
import threading
import time
import urllib2
import StringIO
import gzip
import string
import os
#rewrite SGMLParser for start_a
class Basegeturls(SGMLParser):   
    def reset(self):
        self.url = []
        SGMLParser.reset(self)
    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.url.extend(href)
#for quickly finding
class Newlist(list):
    def find(self, num):
        l = len(self)
        first = 0
        end = l - 1
        mid = 0
        if l == 0:
            self.insert(0,num)
            return False
        while first < end:
            mid = (first + end)/2
            if num > self[mid]:
                first = mid + 1
            elif num < self[mid]:
                end = mid - 1
            else:
                break
        if first == end:
            if self[first] > num:
                self.insert(first, num)
                return False
            elif self[first] < num:
                self.insert(first + 1, num)
                return False
            else:
                return True
        elif first > end:
            self.insert(first, num)
            return False
        else:
            return True

class reptile(threading.Thread):
    def __init__(self, Name, queue, result, Flcok, inittime = 0.00001, downloadway = '.',configfile = 'conf.txt', maxnum = 10000):
        threading.Thread.__init__(self, name = Name)
        self.queue = queue
        self.result = result
        self.Flcok = Flcok
        self.inittime = inittime
        self.mainway = downloadway
        self.configfile = configfile
        self.num = 0      
        self.maxnum = maxnum
        os.makedirs(downloadway + self.getName()) 
        self.way = downloadway + self.getName() + '\\'
    def run(self):
        opener = urllib2.build_opener()   
        while True:
            url = self.queue.get()        
            if url == None:               
                break
            parser = Basegeturls()        
            request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            try:                                         
                page = opener.open(request)
                if page.code == 200:       
                    predata = page.read() 
                    pdata = StringIO.StringIO(predata)
                    gzipper = gzip.GzipFile(fileobj = pdata)
                    try:
                        data = gzipper.read()
                    except(IOError):
                        print 'unused gzip'
                        data = predata
                    try:
                        parser.feed(data)
                    except:
                        print 'I am here'
                    for item in parser.url:
                        self.result.put(item)
                    way = self.way + str(self.num) + '.html'
                    self.num += 1
                    file = open(way, 'w')
                    file.write(data)
                    file.close()
                    self.Flcok.acquire()
                    confile = open(self.configfile, 'a')
                    confile.write( way + ' ' + url + '\n')
                    confile.close()
                    self.Flcok.release()
                page.close()
                if self.num >= self.maxnum:
                    break
            except:
                print 'end error'

class proinsight(threading.Thread):
    def __init__(self, queue, list, homepage, inqueue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.list = list
        self.homepage = homepage
        self.inqueue = inqueue
    def run(self):
        length = len(self.homepage)
        while True:
            item = self.queue.get()
            if item == None:
                break
            if item[0:4] == '\r\n':
                item = item[4:]
            if item[-1] == '/':
                item = item[:-1]
            if len(item) >= len('http://') and item[0:7] == 'http://':
                if len(item) >= length and item[0:length] == self.homepage:
                    if self.list.find(item) == False:
                        self.inqueue.put(item)
            elif item[0:5] == '/java' or item[0:4] == 'java':
                pass
            else:
                if item[0] != '/':
                    item = '/' + item
                item = self.homepage + item
                if self.list.find(item) == False:
                    self.inqueue.put(item)

