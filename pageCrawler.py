#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import logging
from Queue import Queue

logger = logging.getLogger("endlesscode")
file_handler = logging.FileHandler("pageCrawler.log")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler.setFormatter(formatter)
logger.addHander(file_handler)
logger.setLevel(logging.ERROR)

class LinkComsumer(threading.Thread):
    def __init__(self,queue):
        self.queue = queue

    def run(self):
        while True:
          link = self.queue.get()
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
                soup = BeautifulSoup(data)
          except :
               logger('open error url : ' + link)

class LinkFinder(threading.Thread):
    
    visitedUrlPool = set()

    def __init__(self,homepage,queue):
        self.rootContext = homepage
        self.queue = queue
    
    def grabContent(self,link):
        print 'grab content link :' + link
        try:
          req = urllib2.Request(link)
          res = urllib2.urlopen(req)
          content = res.read()
        except Exception,e:
          logger.error('grab url error: '+ link,e)
          content = ""
        return content

    def resolveUrl(self,url = None,contextUrl = None):
        if url is None:
           url = self.rootContext
        else:
           indexNumber = url.rfind('#')
           if indexNumber != -1 :
               url = url[0:indexNumber]            
        import re
        p = re.compile('(http://)(.*)+$')
        matched = p.match(url)
        if matched :
           return url
        if contextUrl is not None and contextUrl.endswith('.html'):
           contextUrl = contextUrl[0:contextUrl.rfind('/')]
        if contextUrl is None or not p.match(contextUrl):
           contextUrl = self.rootContext 
        while(url.startswith('../')):
           if contextUrl.endswith('/'):
              contextUrl = contextUrl[0:contextUrl.rfind('/')]
           contextUrl = contextUrl[0:contextUrl.rfind('/')]          
           url = url[url.find('../') + 3 : len(url)]
        if not contextUrl.endswith('/'):
           contextUrl = contextUrl + '/'           
        return contextUrl + url   

    def tellNewLinks(self,link):
        if link.rfind('#') != -1 :
           return False
        if link.rfind('?') != -1 :
           return False
        if link in self.visitedUrlPool:
           return False
        if not link.startswith(self.rootContext):
           return False
        return True

    def run(self,link = None,contextUrl = None):
        parentLink = self.resolveUrl(link,contextUrl)
        if self.tellNewLinks(parentLink):
           self.visitedUrlPool.add(parentLink)
           page = self.grabContent(parentLink)
           soup = BeautifulSoup(page)
           for frame in soup.find_all('frame'):
               childLink = self.resolveUrl(frame.get('src'),parentLink)
               if self.tellNewLinks(childLink):
                  self.queue.put(childLink)
           for link in soup.find_all('a'):
               childLink = self.resolveUrl(link.get('href'),parentLink)
               if self.tellNewLinks(childLink):
                  self.queue.put(childLink)



if __name__ == "__main__":
    contextUrl = 'http://docs.liferay.com/portal/6.1/javadocs/'    
    pageCrawler = PageCrawler(contextUrl)
    pageCrawler.findLinks()

