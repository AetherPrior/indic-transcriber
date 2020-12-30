import requests
from bs4 import BeautifulSoup

URL = 'https://www.cs.columbia.edu/~hgs/audio/harvard.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('ol')

elem_list = []
for elem in results:
	if(not elem.text.isspace()): 
		text = str(elem.text)
		text = text.strip('\n')
		print(text)
		elem_list.append(text)

with open('transcripts.txt','w') as file:
	for i in elem_list:
		file.write(i+'\n')



