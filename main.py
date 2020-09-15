#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

''' TODO:
[] fill out keywords and pathogens lists 
[] create modules for other publishers (ScienceDirect, etc)
[] refine querying process
'''
import config
import springer as sp
import pprint

# should be relevant to disease traits
keywords = ['pathogenesis', 'incubation period', 'latent period', 
			'infectious period', 'origin', 'reservoir', 'outbreak',
			'host species']

# emerging disease pathogens 
pathogens = ['H1N1', 'Ebola', 'Zika', 'MERS', 'Chikungunya']

# create a text file to list relevant papers
paper_file = open("papers.txt", "w")
json_file = open("json.txt", "w") ### debug use

# generate the query to use
query = sp.generate_query(keywords, pathogens)

# access Springer API to search for papers
# 	usage: request_springer(query, API type, max results)
# documentation to help form queries: https://dev.springernature.com/docs
obj = sp.request_springer(query, 'meta', 500, config.springer_api_key)

pprint.pprint(obj, json_file) ### debug use

# strip irrelevant data, format and write to file
sp.format_results(obj, paper_file)

paper_file.close()
json_file.close() ### debug use
