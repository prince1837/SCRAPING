from   selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
def Zomato_scrap():
	browser = webdriver.Chrome('/usr/bin/chromedriver')
	browser.get("https://www.zomato.com/ncr/great-food-no-bull")
	driver=browser.execute_script("return document.documentElement.outerHTML")
	browser.quit()
	soup=BeautifulSoup(driver,'html.parser')
	div=soup.find('div',class_="ml15 mr15 mt15 " )
	div1=div.find('h1',class_="hero_title collections_title mb5 mt5 ")
	print(div1.text)
	d_name=soup.find('div',class_="row col-res-list collection_listings_container")
	all_r_data=d_name.find_all('div',class_="col-s-8 col-l-1by3")
	empty_list=[]
	link_list={}
	count=1
	for i in all_r_data:
		if(i!=None):
			Dict={}
			rateing=i.find('div',class_="h100 pb20")
			href=rateing.find('a')['href']
			link_list[count]=href
			rate=rateing.find('div')['data-rating']
			Dict["rating"]=rate
			name=rateing.find('div',class_="res_title zblack bold nowrap")
			if name==None:
				continue
			Dict['Resturant-Name']=name.text.strip()
			place=rateing.find('div',class_="nowrap grey-text fontsize5 ttupper").text
			Dict["Place"]=place
			food=rateing.find('div',class_="nowrap grey-text").text.strip()
			Dict["Cuisines"]=food
			empty_list.append(count)
			empty_list.append(Dict)
			count+=1
	pprint(empty_list)
	user=int(input("Which hotel do you want to know about?...       \n"))
	for i,j in link_list.items():
		if i==user:
			hotel={}
			browser = webdriver.Chrome('/usr/bin/chromedriver')
			browser.get(j)
			driver=browser.execute_script("return document.documentElement.outerHTML")
			browser.quit()
			soup=BeautifulSoup(driver,'html.parser')
			if(soup!=None):
				all_detail=soup.find('div',class_="row ui segment")
				if(all_detail!=None):
					phone=all_detail.find('',class_="mbot")
					contact=phone.find('span',class_="tel").text
					hotel["contact no..."]=contact.strip()
					cost=all_detail.find('div',class_="res-info-detail")
					cost1=cost.find('span',tabindex="0").text.strip()
					hotel["Average-coast"]=cost1
					hours=all_detail.find('div',class_="medium").text
					hotel["Opening-time"]=hours
					more=all_detail.find('div',class_="res-info-highlights")
					more_d=more.find_all('div',tabindex="0")
					det_list=[]
					for i in more_d:
						det=i.find('div',class_="res-info-feature-text").text
						det_list.append(det)
					hotel["More-information"]=det_list
					feature=all_detail.find('div',class_="ln24")
					span=feature.find_all('span')
					f1=[]
					for i in span:
						feat=i.find('a').text
						f1.append(feat)
					hotel["Featured in collections"]=f1
	return(hotel)
pprint(Zomato_scrap())