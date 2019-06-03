import requests
from bs4 import BeautifulSoup
import json
import os.path
from os import path
import pprint
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
top_250=(scrap_top_list())
storage = {}
allyear = []
for movie in top_250:
	if movie["year"] not in allyear:
		allyear.append(movie["year"])
allyear.sort()
for year in allyear:
	Y = []
	for i in top_250:
		if i["year"] == year:
			Y.append(i)
	storage[year] = Y
pprint.pprint(storage)


			
	

