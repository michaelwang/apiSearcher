import threading
import urllib2
import StringIO
import gzip
import string
from bs4 import BeautifulSoup
from Queue import Queue
import os

class LinksFinder(threading.Thread):
     def __init__(self,homepage,queue):
         threading.Thread.__init__(self)                  
         self.homepage = homepage
         self.queue = queue 

     def resolveUrl(self,url = None,contextUrl = None):
        if url is None:
           url = self.homepage
        else:
           indexNumber = url.rfind('#')
           if indexNumber != -1 :
               return None
           if url.rfind('?') !=  -1 :
               return None

        import re
        p = re.compile('(http://)(.*)+$')
        matched = p.match(url)
        if matched :
           if not url.startswith(self.getRootContext()):
              return None            
           return url
        if contextUrl is None or not p.match(contextUrl):
           contextUrl = self.homepage
        if contextUrl.endswith('.html'):
           contextUrl = contextUrl[0:contextUrl.rfind('/')]           
        while(url.startswith('../')):
           if contextUrl.endswith('/'):
              contextUrl = contextUrl[0:contextUrl.rfind('/')]
           contextUrl = contextUrl[0:contextUrl.rfind('/')]          
           url = url[url.find('../') + 3 : len(url)]
        if not contextUrl.endswith('/'):
           contextUrl = contextUrl + '/'           
        return contextUrl + url   

     def run(self):
         data = readPage(self.homepage)
         if data is not None:
            soup = BeautifulSoup(data)
            allLinks = soup.find_all('a')
            print len(allLinks)
            for link in allLinks:
                originalUrl = link.get('href')
                resolvedUrl = self.resolveUrl(originalUrl,self.homepage)
                if resolvedUrl is None:
                      continue
                self.queue.put(resolvedUrl,timeout=3)  

def readPage(url):
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    try:
       print 'begin open page'
       page = opener.open(request)
       if page.code == 200:
          print 'begin read page'
          data = page.read()
          print 'after read page'
          page.close()
    except:
       print 'end error'
       data = None
    return data

class Reptile(threading.Thread):
     def __init__(self,queue,visitedUrlPool,index,folder):
         threading.Thread.__init__(self)         
         self.queue = queue
         self.visitedUrlPool = visitedUrlPool
         self.folder ='./' +  folder
         self.name = index
         if not os.path.exists(self.folder):
            os.makedirs(self.folder)

     def getRootContext(self):
         if homepage.endswith('.html'):
            contextUrl = homepage[0:homepage.rfind('/')]
            return contextUrl
         else:
            return homepage

     def getFileName(self,link):
         name = link[link.rfind('/') + 1: len(link)]
         return name

     def run(self):
         while 1:
            if self.queue.empty():
               print 'Thread:' + self.name + ' no data,die'
               break               
            link = self.queue.get(timeout=3)
            print 'Thread ' + self.name + ':' + link 
            data = readPage(link)
            if data is not None:
               way = self.folder + '/' + self.getFileName(link)
               file = open(way,'w')
               file.write(data)
               file.close()
            else:
               continue

if __name__ == '__main__':
#   homepage = 'http://docs.liferay.com/portal/6.1/javadocs/allclasses-noframe.html'
   homepage = 'http://struts.apache.org/development/2.x/struts2-core/apidocs/allclasses-noframe.html'
#   homepage = 'http://docs.liferay.com/portal/6.1/javadocs/com/liferay/portal/kernel/test/AbstractIntegrationJUnitTestRunner.html'
   queue = Queue()
   queue.put(homepage)
   
   visitedUrlPool = set()
   
   linksFinder = LinksFinder(homepage,queue)
   linksFinder.start()

   folder = 'struts2'
   
   reptile = Reptile(queue,visitedUrlPool,10,folder)
   reptile.start()
   

   import time
   for i in range(4):
       time.sleep(1)
   print 'wake up now'
       
   
   for i in range(12):
       reptile = Reptile(queue,visitedUrlPool,i,folder)
       reptile.start()


   
