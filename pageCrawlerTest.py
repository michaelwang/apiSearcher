import unittest
from pageCrawler import PageCrawler 

class TestPageCrawler(unittest.TestCase):

   instance = None;
   
   def setUp(self):
       self.instance = PageCrawler('')
    
   def testResolveUrl(self):
       url = '../../../a.html'
       contextUrl = 'http://a/b/c/d/'
       expectedUrl = 'http://a/a.html'
       actualUrl = self.instance.resolveUrl(url,contextUrl)
       self.assertEqual(expectedUrl,actualUrl)
       contextUrl = 'http://a/b/b/d'
       actualUrl = self.instance.resolveUrl(url,contextUrl)
       self.assertEqual(expectedUrl,actualUrl)
       url = 'http://ab/cc/sss.html'
       expectedUrl = url
       self.assertEqual(expectedUrl,self.instance.resolveUrl(url,contextUrl))
       contextUrl = 'http://test/a/b/c/dd.html'
       url = 'd/e/f/g/h/a.html'
       expectedUrl = 'http://test/a/b/c/d/e/f/g/h/a.html'
       self.assertEqual(expectedUrl,self.instance.resolveUrl(url,contextUrl))
#       contextUrl = 'http://docs.liferay.com/portal/6.1/javadocs/com/liferay/portal/service/persistence/package-summary.html'
       contextUrl = 'http://docs.liferay.com/portal/6.1/javadocs/com/liferay/portal/kernel/dao/orm/BaseActionableDynamicQuery.html#setInterval(int)'
    #   url = '../../../../../com/liferay/portal/service/persistence/BatchSession.html'
       url = '../../../../../com/liferay/portal/service/persistence/RepositoryEntryPersistence.html'
       expectedUrl = 'http://docs.liferay.com/portal/6.1/javadocs/com/liferay/portal/service/persistence/RepositoryEntryPersistence.html'
       self.assertEqual(expectedUrl,self.instance.resolveUrl(url,contextUrl))

       contextUrl ='http://docs.liferay.com/portal/6.1/javadocs/com/liferay/util/bridges/jsf/icefaces/package-summary.html'
       url = ''
       
if __name__ == '__main__':
   unittest.main()
   
