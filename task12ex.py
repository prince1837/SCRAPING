import requests
from bs4 import BeautifulSoup
import json
import os.path
from os import path
from pprint import pprint
def scrap_top_list():
	if os.path.exists("movie.json"):
		with open ("movie.json",'r') as file:
			read=file.read()
			main_data=json.loads(read)
			return(main_data)
	else:
		url=" https://www.imdb.com/india/top-rated-indian-movies/"
		page=requests.get(url)
		soup=BeautifulSoup(page.text,'html.parser')
		main_div=soup.find('div',class_="lister")
		div=main_div.find('tbody',class_="lister-list")
		trs=div.findAll('tr')
		num=0
		main_data=[]
		for tr in trs:
			num=num+1
			dic={}
			title_colum=tr.find('td',class_="titleColumn").a
			dic['name']=title_colum.get_text()
			dic['position']=num
			year=tr.find('span',class_="secondaryInfo")
			new_year=year['year']=year.get_text()
			cut=int(new_year[1:5])
			dic['year']=cut
			movie_rateing=tr.find('td',class_="ratingColumn imdbRating")
			rateing=movie_rateing.get_text()
			cut_rateing=float(rateing[3:5])
			dic['rateing']=cut_rateing
			dic['url']="https://www.imdb.com"+title_colum["href"][:17]
			main_data.append(dic)
		with open("movie.json","w") as file:
			read = json.dumps(main_data)
			file.write(read)
			file.close()
		return(main_data)
top_movies=scrap_top_list()
def scrap_movie_cast(movie_cast_url):
	if os.path.exists("movie_cast.json"):
		with open ("movie_cast.json",'r') as file:
			read=file.read()
			main_data=json.loads(read)
			return(main_data)
	else:
		c_data={}
		count=1
		for i in movie_cast_url:
			url=(i["url"])
			page=requests.get(url)
			soup=BeautifulSoup(page.text,'html.parser')
			div=soup.find_all('div',class_="see-more")
			for i in div:
				if "See full cast »"==i.text.strip():
					cast=i.find('a').get("href")
			url1=url+cast
			page1=requests.get(url1)
			bs4=BeautifulSoup(page.text,'html.parser')
			table=bs4.find('table',class_="cast_list")
			tbody=table.find_all('tr')
			cast_data=[]	
			for i in tbody:
				td=i.find_all('td',class_="")
				for j in td:
					a=j.find('a')
					Id=a.get('href')[6:15]
					name=a.text.strip()
					dict1={"imdb_id":Id,
					"name":name}
					cast_data.append(dict1)
			c_data["cast of "+str(count)+" movie"]=cast_data
			count+=1
		with open("movie_cast.json","w") as file:
				read1 = json.dumps(c_data)
				file.write(read1)
				file.close()
	return(c_data)

pprint(scrap_movie_cast(top_movies))