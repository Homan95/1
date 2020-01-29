from requests import get
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from difflib import ndiff


engine=create_engine('sqlite:///Parsing_base.db', echo=False)
base=declarative_base()

class DbItem(base):
	__tablename__='Parsing'
	id=Column(Integer, primary_key=True)
	url=Column(String)
	title=Column(String)
	soup=Column(String)

base.metadata.create_all(engine)

sesion=sessionmaker(bind=engine)()

class Result:
	def __init__(self,url,headers):
		self.result=get(url,headers)
		self.soup=BeautifulSoup(self.result.text, features="lxml")
		self.url=url
		self.title=self.soup.title

htmlpage='https://foootball-blog.blogspot.com/2019/05/chelsi-ajjntrakht-prevyu.html'
headers = {'User-agent' : 'Mozilla/5.0'}

a=Result(htmlpage, headers)

to_extract = (a.soup.findAll('script'), a.soup.findAll('style'))
for extract in to_extract:
	for item in extract:
	    item.extract()

Page_a=DbItem(url=str(a.url), soup=str(a.soup), title=str(a.title))

sesion.add(Page_a)

sesion.commit()

q=sesion.query(DbItem)

if q[-1].soup==q[-2].soup :
	print("Змін не було")
else:
	a=q[-1].soup.splitlines(1)
	b=q[-2].soup.splitlines(1)
	print (''.join(ndiff(a, b)) )
