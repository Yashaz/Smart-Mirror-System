import requests
from bs4 import BeautifulSoup
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import os
def getmovie():
	target = open('emo.txt','r')
	emot = target.read()
	lst = emot.split(",")
	if os.path.exists('movie.txt'):
		os.remove('movie.txt')
	for il in lst[1:]:

		url1 = 'https://agoodmovietowatch.com/mood/'
		url = url1+il  
		print url
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')

		result = soup.find_all("a",title=True,class_="filldiv")
		#result = soup.find_all("a","title")
		"""
		if lst[0]=='happy':
			f=open('happy.txt',"a")
		elif lst[0]=='sad':
			f=open('sad.txt',"a")
		elif lst[0]=='anger':
			f=open('anger.txt',"a")
		elif lst[0]=='neutral':
			f=open('neutral.txt',"a")
		elif lst[0]=='surprise':
			f=open('surprise.txt',"a")
		"""
		f = open('movie.txt','a')
		for i in result:
			j=i['title']
			j=j[:-7]
			f.write(j.encode('ascii', 'ignore').decode('ascii'))
			f.write("\n")
		f.close()
	target.close()



getmovie()

