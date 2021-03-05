#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import config
import pprint
import time
import re
import copy
import os
import springer as sp
from text_scraper import get_fulltext

''' Global variables '''
# these store data from disease_list.txt and trait_list.txt
diseases = []
traits = []

''' call_springer
Puts API calls in to the Springer Database 
Stores results in 'papers.txt' and 'raw.txt' in ./data/springer.

Params: query, the string to be entered in the search
		nresults, the number of results to be returned per query
'''
def call_springer(query, nresults):
	# create text files to store the data
	fp= "./data/springer/"
	with open(fp+"papers.txt", "w") as papers, open(fp+"raw.txt", "w") as raw:

		# access Springer API to search for papers
		# usage: request_springer(query, API type, results per page, starting position)
		# documentation to help form queries: https://dev.springernature.com/docs
		'''for page in range(1, 20, 20):
			obj = sp.request_springer(query, 'open', 10, config.springer_api_key, 1)
			if obj == '':
				continue
			else:
				pprint.pprint(obj, raw)

				# strip irrelevant data, format and write to file
				sp.format_results(obj, papers)
		'''
		obj = sp.request_springer(query, 'open', nresults, config.springer_api_key, 1)
		pprint.pprint(obj, raw)
		sp.format_results(obj, papers)
		
''' generate_query
Formats strings from disease_list.txt and trait_list.txt into
search queries (also strings). 

params: disease - a list containing the name(s) of the disease
		trait - a list containing the trait information
output: returns a string containing the query
'''
def generate_query(disease, trait):
	query = ''
	
	# makes it only return journal articles
	query = 'type:Journal '
	
	# group alternate names using OR and parentheses
	query += '('
	query += 'title:' # only search for articles with disease in title
	query += r' OR title:'.join(disease)
	query += ')'
	
	# use logical AND to link disease + trait info
	query += ' AND '
	
	# trait terms should have internal grouping, just put parens outside
	query += '(' + trait + ')'
	
	# adding (emerging infecti* disease* OR EID*) to query to narrow results
	#query += ' AND (emerging infecti* disease* OR EID*)'

	'''
	End result should look something like:
	(title:COVID-19 OR title:Sars-COV-2) AND 
		(asymptomatic AND (proportion OR ratio))
	'''
	
	return query
	
''' get_disease_data
Reads './search_parameters/disease_list.txt', extracts the list of 
disease names and formats it into a list called 'diseases'.
'''
def get_disease_data():
	with open(r'./search_parameters/disease_list.txt', 'r') as disease_file:
	
		# might use later to index disease info
		line_counter = 0 
		
		# create a 2d list of diseases and alternate names for them
		for line in disease_file:
			# skip the header
			if line[0] == '+' or line[0] == '\n':
				line_counter += 1
				continue
				
			# split by comma and add the names to 'diseases' top-level list
			tmp = [word.rstrip('\n') for word in line.split(', ')]
			diseases.append(tmp)
			line_counter += 1

''' get_trait_data
Reads './search_parameters/trait_list.txt', extracts the list of trait
information and formats it into a list called 'traits'.
'''
def get_trait_data():
	with open(r'./search_parameters/trait_list.txt', 'r') as trait_file:
		
		# might use later to index trait info
		line_counter = 0 
		
		# parse the file
		for line in trait_file:
			# skip the header/instructions/etc
			if line[0] == '+' or line[0] == '\n':
				line_counter += 1
				continue
				
			# add the whole line to the list
			traits.append(line.rstrip('\n'))	
			line_counter += 1

''' get_text
Scapes the full-text of open access papers and stores in './texts/'
Params: url, a string representing the url of the paper
Returns: 0 if it was successful, -1 if the file already exists
'''
def get_text(url, cur_disease):
	
	'''
	name text file according to this convention:
		-split doi along slash
		-create folder name with left side
		-create file name with right side
		-place file in folder
		-full doi can be easily obtained by combining them
	'''
	# set up the filesystem where it's going to be saved
	doi = url.lstrip('http://dx.doi.org/')
	names = doi.split('/')
	folder_name = names[0]
	file_name = names[1]
	
	# make directory with folder_name where you store full texts
	# first check if the dir already exists
	txt_path = './data/texts/'+cur_disease+'/'+folder_name+'/'
	if not os.path.exists(txt_path):
		os.mkdir(txt_path)
		
	# add file name to the path
	txt_path += file_name+'.txt'
	
	# check if it's already been scraped
	if os.path.exists(txt_path):
		print("\tSkipped. Already present in system.")
		return -1
	
	# get the full text 
	text_as_string = get_fulltext(url)
	
	# skip if it doesn't get the full text
	if len(text_as_string) < 1000:
		return -1
	else:
		with open(txt_path, 'w') as text:
			text.write(text_as_string)
	
	return 0

''' iterative_search
This will iteratively search for each disease in disease_list matched
with each trait in trait_list and scrape the texts.

params: nresults, the number of results to return for each disease +
		trait query
'''
def iterative_search(nresults):
	for disease in diseases:
		disease_path = './data/texts/'+disease[0]
		if not os.path.exists(disease_path):
			os.mkdir(disease_path)
			
		time.sleep(1) # to not go over api limit
		for trait in traits:
			# create search string
			query = generate_query(disease, trait)

			print("current query: " + query)
			
			# Pass query to the API
			call_springer(query, nresults)

			# get full texts of papers in ./data/springer/papers.txt
			with open('./data/springer/papers.txt', 'r') as papers:
				print('Scraping papers:')
				for line in papers:
					if 'URL:' in line:
						url = papers.readline()
						url = url.strip('\n\t')
						print(url)
						time.sleep(0.01)
						get_text(url, disease[0])
					else: 
						continue
						
''' single_search
Performs a single query

Params: disease, a string containing the name of the disease + alternate names
				separated by commas
		trait, a string contining the trait you want to include in the search
				you can use booleans and wildcards
		nresults, the number of results that are returned from the search
'''						
def single_search(disease, trait, nresults):
	# put disease names into a list
	disease_lst = [word for word in disease.split(', ')]
	
	query = generate_query(disease_lst, trait)
	
	call_springer(query, nresults)
	
	# get full texts of papers in ./data/springer/papers.txt
	with open('./data/springer/papers.txt', 'r') as papers:
		print('Scraping papers:')
		for line in papers:
			if 'URL:' in line:
				url = papers.readline()
				url = url.strip('\n\t')
				print(url)
				time.sleep(0.01)
				get_text(url, disease[0])
			else: 
				continue	
						
''' Main '''
# Load up most recent data from disease_list and trait_list
get_disease_data()
get_trait_data()

#iterative_search(5)




