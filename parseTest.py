import unittest
from parse import Parser,Class,Method,Builder
from bs4 import BeautifulSoup
import sqlite3

class TestParser(unittest.TestCase):
    def setUp(self):
     self.instance = Parser()
     self.builder = Builder()

    def testBuild(self):
        filePath = '/home/michael/Downloads/hibernate-release-4.3.5.Final/documentation/javadocs/org/hibernate/'                
        self.builder.buildDBEngine(filePath)
    '''
    def testParseMethod(self):
     parsedFile = '/home/michael/Downloads/hibernate-release-4.3.5.Final/documentation/javadocs/org/hibernate/UnresolvableObjectException.html'        
     soup = BeautifulSoup(open(parsedFile))
     methods = self.instance.parseMethods(soup)

    def testParse(self):
     parsedFile = '/home/michael/Downloads/hibernate-release-4.3.5.Final/documentation/javadocs/org/hibernate/UnresolvableObjectException.html'
     self.instance.parseAndSaveDB(parsedFile)

     conn = sqlite3.connect('hibernate4.3.5.db')
     cur = conn.cursor()
     cur.execute('select * from classes')

     for row in cur:
         print row
     cur.execute('select * from methods')
     for row in cur:
         print row
     conn.close()    
    '''

if __name__ == '__main__':
    unittest.main()
