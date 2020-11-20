#!/usr/bin/env python3
# citations.py - pulls citations from article urls

'''
Warning: This will take a long time to run depending on how the 
		 citation servers feel on any given day.
'''

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
cited = {} # dictionary for if one source is found multiple times
# get the citations for each article and store them in a string to be written to a file
for doi in df['Article URL']:
	if type(doi) is not str:
		continue
		cur_line += 1
	else:
		# if the source is already cited, just copy it
		if doi in cited:
			txt += str(cur_line) + '\n'
			txt += cited[doi] + '\n'
			cur_line += 1 
			continue
			
		# if it's not already cited, request the citation from the server
		while(True):
			try:
				response = requests.get(doi, headers=headers)
				response.encoding = 'utf-8'
				print(str(cur_line) + ': ' + str(response.status_code))
				if(response.status_code == 200):
					break
			except Exception as inst:
				print(inst)
		# add the citation to the text string and increment cur_line
		txt += str(cur_line) + '\n'
		txt += str(response.text) + '\n\n'
		cited[doi] = response.text
		cur_line += 1

# write the citations to a file
with open(cwd+'/database/citations.txt', 'w+') as cites:
	cites.write(txt)

	
