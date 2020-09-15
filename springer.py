#!/usr/bin/env python3
# springer.py is a script to find relevant journal articles from  
# 	Springer Databases (Nature, etc)
# Springer API documentation: https://dev.springernature.com/docs

import requests

''' request_springer
	parameters: query 	- keywords that you are searching for
				api	  	- API type (open or meta)
				num 	- max number of results 
				key 	- your API key
	output: json object with search results 
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




