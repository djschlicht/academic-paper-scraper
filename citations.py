#!/usr/bin/env python3
# citations.py - pulls citations from article urls

import pandas as pd
import requests

# specify what kind of citation to get
headers = {'Accept': 'text/x-bibliography; style=apa'}

# get the article doi-urls
df = pd.read_csv('./database/db.csv', usecols=["Article URL"])

txt = ''
cur_line = 2 # first row is headers and csv usually not 0 indexed
# get the citations for each article and store them in a string to be written to a file
for doi in df['Article URL']:
	if type(doi) is not str:
		continue
		cur_line += 1
	else:
		response = requests.get(doi, headers=headers)
		if(response.status_code != 200):
			print("error: status code" + str(response.status_code))
		response.encoding = 'utf-8'
		txt += str(cur_line) + '\n'
		txt += str(response.text) + '\n\n'
		cur_line += 1

# write the citations to a file
with open('./database/citations.txt', 'w+') as cites:
	cites.write(txt)

	
