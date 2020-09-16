#!/usr/bin/env python3
# elsevier.py - 

import requests

''' query_elsevier
	parameters: q 	- the query text
				key - API key
				s 	- start
				c 	- count
	output: a list of documents matching query and their metadata and URIs
'''
def query_elsevier(q, key, s, c):
	url = 'https://api.elsevier.com/content/search/scidir?'
	parameters = {
		'query': q,
		'APIKey': key,
		'start': str(s),
		'count': str(c)
	}
	
