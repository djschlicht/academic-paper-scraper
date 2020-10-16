#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import config
import pprint
import time
import re
import copy
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
		for page in range(1, 450, 50):
			obj = sp.request_springer(query, 'open', 50, config.springer_api_key, page)
			pprint.pprint(obj, raw)

			# strip irrelevant data, format and write to file
			sp.format_results(obj, papers)

''' generate_query()
Formats strings from disease_list.txt and trait_list.txt into
search queries (also strings). 

params: disease - a list containing the name(s) of the disease
		trait - a list containing the trait information
output: returns a string containing the query
'''
def generate_query(disease, trait):
	
	# group alternate names using OR and parentheses
	query = '('	
	query += r' OR '.join(disease)
	query += ')'
	
	# use logical AND to link disease + trait info
	query += ' AND '
	
	# trait terms should have internal grouping, just put parens outside
	query += '(' + trait + ')'
	
	# adding (emerging infecti* disease* OR EID*) to query to narrow results
	query += 'AND (emerging infecti* disease* OR EID*)'

	'''
	End result should look something like:
	(COVID-19 OR Sars-COV-2 OR "novel coronavirus") AND 
		(asymptomatic AND (proportion OR ratio OR percent*))
	'''

	# TODO: add extra filters e.g. date restriction, journal, etc
	
	return query
	
''' get_disease_data()
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

''' get_trait_data()
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


''' Main '''
# Load up most recent data from disease_list and trait_list
get_disease_data()
get_trait_data()

# Build the search string
query = generate_query(diseases[3], traits[7])

# Test on the API - works great now to refine searches
#call_springer(query)

# Test of getting full text open access papers (roundaboutly)
get_text('./texts/tmp_pdf/lyons.pdf')
'''
with open('./useful_papers.txt', 'r') as up:
	for line in up:
		get_text(line)
'''

''' Uncomment to print 
diseases and traits list to stdout

pp = pprint.PrettyPrinter(indent=1)
print("Disease and Names:")
pp.pprint(diseases)
print()
print("Trait Strings:")
pp.pprint(traits)
print()
'''

