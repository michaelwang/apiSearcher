from bs4 import BeautifulSoup
import sqlite3

class Method():
      def __init__(self,name,description):
          self.name = name
          self.description = description

class Class():
      def __init__(self,name,package,description):
          self.name = name
          self.description = description
#          self.signature = signature
          self.package = package

class Package():
      def __init__(self,name,description,signature):
          self.name = name
          self.description = description
          self.signature = signature

class Builder():
      def buildDBEngine(self,path):
          parser = Parser()
          from os import walk
          from os.path import join
          stopFiles = ["package-summary.html","package-frame.html","package-tree.html","package-use.html"]
          stopDirNames = ['class-use']
          for (dirpath,dirnames,filenames) in walk(path):
               if dirpath.find('class-use') == -1:
                  for filename in filenames:
                     if filename not in stopFiles:
                        absolutePath = join(dirpath,filename)
                        print absolutePath                    
                        parser.parseAndSaveDB(absolutePath)


class Parser():
      def parseAndSaveDB(self,page):
          soup = BeautifulSoup(open(page))
          classObj = self.parseClass(soup)
          methods = self.parseMethods(soup)
          self.saveDB(classObj,methods)
          
      def parseClass(self,soup):
          className = soup.h2.string
          packageName = soup.find('div',class_='subTitle').string
          description = soup.find('div',class_='description').find('div',class_='paragraph')
          if description is not None:
             description = description.p.string
          else:
             description = "None"
          classObj = Class(className,packageName,description)
          return classObj

      def parseMethods(self,soup):
          methods = []
          methodBlock = soup.find('div',class_='details')
          if methodBlock is not None:
            h4List = methodBlock.find_all('h4')
            for h4 in h4List:
              m = h4.parent
              if m.p is None:
                  des = "None"
              else:
                  des = m.p.string              
              method = Method(m.h4.string,des)
              methods.append(method)
          return methods

      def saveDB(self,classObj,methods):
          conn = sqlite3.connect('hibernate4.3.5.db')
          cur = conn.cursor()
          cur.execute('''CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY autoincrement not null,class_name VARCHAR(100),package VARCHAR(200), description TEXT)''')
          cur.execute('INSERT INTO classes (class_name,package,description) VALUES(?,?,?)',[classObj.name,classObj.package,classObj.description])
          cur.execute('''CREATE TABLE IF NOT EXISTS methods (id INTEGER PRIMARY KEY autoincrement not null,name VARCHAR(100),description TEXT)''')
          for m in methods:
             cur.execute('INSERT INTO methods (name,description) VALUES(?,?)',[m.name,m.description])
          conn.commit()
          conn.close()
          
       
          
          
          
          
