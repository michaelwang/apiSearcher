from bs4 import BeautifulSoup
import sqlite3

class Method():
      def __init__(self,name,description):
          self.name = name
          self.description = description

class Class():
      def __init__(self,name,package):
          self.name = name
#          self.description = description
#          self.signature = signature
          self.package = package

class Package():
      def __init__(self,name,description,signature):
          self.name = name
          self.description = description
          self.signature = signature


class Parser():
      def parseAndSaveDB(self,page):
          soup = BeautifulSoup(open(page))
          classObj = self.parseClass(soup)
          methods = self.parseMethods(soup)
          self.saveDB(classObj,methods)
          
      def parseClass(self,soup):
          className = soup.h2.string
          packageName = soup.h2.previous_sibling.previous_sibling.string
          classObj = Class(className,packageName)
          return classObj

      def parseMethods(self,soup):
          methods = []
          constructor = soup.find('div',class_='details').find('ul').find('li').find('ul')
          method = Method(constructor.h4.string,constructor.p.string)
          methods.append(method)
          ms = constructor.next_sibling.next_sibling.next_sibling.next_sibling.find_all('ul')
          for m in ms:
              des = ""
              if m.p is None:
                  des = "None"
              else:
                  des = m.p.string
              method = Method(m.h4.string,des)
              methods.append(method)
          return methods

      def saveDB(self,classObj,methods):
          conn = sqlite3.connect('struts2.db')
          cur = conn.cursor()
          cur.execute('''CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY autoincrement not null,class_name VARCHAR(100),package VARCHAR(200), description TEXT)''')
          cur.execute('INSERT INTO classes (class_name,package) VALUES(?,?)',[classObj.name,classObj.package])
          cur.execute('''CREATE TABLE IF NOT EXISTS methods (id INTEGER PRIMARY KEY autoincrement not null,name VARCHAR(100),description TEXT)''')
          for m in methods:
             cur.execute('INSERT INTO methods (name,description) VALUES(?,?)',[m.name,m.description])
          conn.commit()
          conn.close()
          
       
          
          
          
          
