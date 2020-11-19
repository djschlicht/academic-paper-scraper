#!/usr/bin/env python3
# citations.py - pulls citations from article urls

import pandas as pd
import requests
import os

# get working dir
cwd = os.getcwd()

# specify what kind of citation to get
headers = {'Accept': 'text/x-bibliography; style=apa'}

# get the article doi-urls
df = pd.read_csv(cwd+'/database/db.csv', usecols=["Article URL"])

txt = ''
cur_line = 2 # first row is headers and csv usually not 0 indexed
# get the citations for each article and store them in a string to be written to a file
for doi in df['Article URL']:
	if type(doi) is not str:
		continue
		cur_line += 1
	else:
		while(True):
			try:
				response = requests.get(doi, headers=headers)
				response.encoding = 'utf-8'
				if(response.status_code == 200):
					break
			except Exception as inst:
				print(inst)
		txt += str(cur_line) + '\n'
		txt += str(response.text) + '\n\n'
		cur_line += 1

# write the citations to a file
with open(cwd+'/database/citations.txt', 'w+') as cites:
	cites.write(txt)

	
