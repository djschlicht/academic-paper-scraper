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
'''
def call_springer(query):
	# create text files to store the data
	fp= "./data/springer/"
	with open(fp+"papers.txt", "w") as papers, open(fp+"raw.txt", "w") as raw:

		# access Springer API to search for papers
		# usage: request_springer(query, API type, results per page, starting position)
		# documentation to help form queries: https://dev.springernature.com/docs
		for page in range(1, 50, 20):
			obj = sp.request_springer(query, 'open', 20, config.springer_api_key, page)
			pprint.pprint(obj, raw)

			# strip irrelevant data, format and write to file
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
	
	# TODO: add extra filters e.g. date restriction, journal, etc

	# restrict to journal articles
	query += 'type:Journal '
	
	# group alternate names using OR and parentheses
	query += '('	
	query += r' OR '.join(disease)
	query += ')'
	
	# use logical AND to link disease + trait info
	query += ' AND '
	
	# trait terms should have internal grouping, just put parens outside
	query += '(' + trait + ')'
	
	# adding (emerging infecti* disease* OR EID*) to query to narrow results
	query += ' AND (emerging infecti* disease* OR EID*)'

	'''
	End result should look something like:
	(COVID-19 OR Sars-COV-2 OR "novel coronavirus") AND 
		(asymptomatic AND (proportion OR ratio OR percent*))
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
def get_text(url):
	
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
	txt_path = './texts/'+folder_name+'/'
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
	
	with open(txt_path, 'w') as text:
		text.write(text_as_string)
	
	return 0

''' Main '''
# Load up most recent data from disease_list and trait_list
get_disease_data()
get_trait_data()

# Build the search string
query = generate_query(diseases[5], traits[3])

# Pass query to the API
call_springer(query)

# get full texts of papers in ./data/springer/papers.txt
with open('./data/springer/papers.txt', 'r') as papers:
	print('Scraping papers:')
	for line in papers:
		if 'URL:' in line:
			url = papers.readline()
			url = url.strip('\n\t')
			print(url)
			get_text(url)
		else: 
			continue
