#!/usr/bin/env python3
# springer.py has functions to access Springer API and find articles from 
# 	Springer Databases (Nature, etc)
# Springer API documentation: https://dev.springernature.com/docs

import requests

''' request_springer
	parameters: query 	- keywords that you are searching for
				api	  	- API type (open or meta)
				num 	- max number of results 
				key 	- your API key
	output: json object (really a dict) with search results 
'''
def request_springer(query, api, num, key):
	# set API url and error check
	if api == 'meta':
		url = 'http://api.springernature.com/metadata/json?'
	elif api == 'open':
		url = 'http://api.springer.com/openaccess/json?'
	else:
		print("Invalid API param. Choose 'meta' or 'open'.")
		return -1
	if not isinstance(query, str):
		print("Invalid query. Check the documentation: https://dev.springernature.com/docs")
		return -1
	
	# set parameters, make the request, return results
	parameters = {
		'q': query,
		#'s': '1',  	# index of first hit to return (optional)
		'p': str(num),
		'api_key': str(key)
	}
	response = requests.get(url, params=parameters)
	return response.json()
	
''' format_results
	parameters: obj	- a json object (really a dict) to format
				f	- a text file to write to
'''
def format_results(obj, f):
	# get total number of results
	num_results = obj['result'][0]['recordsDisplayed']

	# for each result, format it and write to file
	for res in obj['records']:
		if not isinstance(res['title'], str): # if title isnt a string, move along
			continue
		f.write('Title: \n\t' + res['title'] + '\n')
		f.write('Publisher and Journal: \n\t' + res['publisher'] + 
			'; ' + res['publicationName'] + '\n')
		f.write('Publication Date: \n\t' + res['publicationDate'] + '\n')
		f.write('Authors:\n')
		for auth in res['creators']:
			f.write('\t' + auth['creator'] + '\n')
		f.write('Abstract:\n\t')
		if res['abstract'] == '':
			f.write('N/A \n')
		else:
			f.write(res['abstract'] + '\n')
		f.write('DOI: \n\t' + res['doi'] + '\n')
		f.write('URL: \n\t' + res['url'][0]['value'] + '\n\n\n')
		
''' generate_query
	parameters: key - keywords/traits/etc
				path- pathogens
	output:		a well crafted search term
'''
def generate_query(key, path):
	# '("path1" OR "path2" OR ...) AND ("key1" OR "key2" ...)'
	query = r'("'
	for p in path[:-1]:
		query = query + p + r'" OR "'
	query = query + path[-1] + r'") AND ("'
	for k in key[:-1]:
		query = query + k + r'" OR "'
	query = query + key[-1] + r'")'
	# AND -(year:2021)
	query = query + r' AND -(year:2021)'
	return query
	
	




