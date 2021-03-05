# citations.py
# Cite papers from their URL

import pandas as pd
import requests
import os

def cite_doi(path, column):
	"""Write file containing citations from all rows with DOI link
	
	Arguments:
	path	-- the path to the csv (e.g. '../data.csv')
	column	-- name of column with urls
	"""
	
	# specify what kind of citation - sent to doi citation server
	headers = {'Accept': 'text/x-bibliography; style=apa'}
	df = pd.read_csv(path, usecols=[column])
	txt = ''
	cur_row = 2 # csv is 1 indexed and first line is col names
	cited = {}

	for doi in df['URL']:
		if "doi.org" not in doi:
			continue
			cur_row += 1
			
		else:
			# pull duplicates from cited
			if doi in cited:
				txt += str(cur_row) + '\n'
				txt += cited[doi] + '\n'
				cur_row += 1 
				continue

			while(True):
				try:
					response = requests.get(doi, headers=headers)
					response.encoding = 'utf-8'
					# only add to citations if server responds
					if(response.status_code == 200):
						break
				except Exception as inst:
					print(inst)

			txt += str(cur_line) + '\n'
			txt += str(response.text) + '\n\n'
			cited[doi] = response.text
			cur_line += 1

	cwd = os.getcwd()
	with open(cwd + 'citations.txt', 'w+') as citations:
		citations.write(txt)

# TODO: add functions for other document ID types (PMID, etc)
