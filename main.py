#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import config
import pprint
import time
import springer as sp

''' Global variables '''
diseases = []
traits = []

''' Functions ''' 
''' call_springer()
This function will put API calls into the Springer Database and store
the results in the files 'papers.txt' and 'raw.txt' in ./data/springer.
'''
def call_springer():
	# create text files to store the data
	paper_file = open(r"./data/springer/papers.txt", "w")
	raw_file = open(r"./data/springer/raw.txt", "w")

	# generate the query to use
	query = generate_query(keywords, pathogens)

	# access Springer API to search for papers
	# 	usage: request_springer(query, API type, results per page, starting position)
	# documentation to help form queries: https://dev.springernature.com/docs
	for page in range(1, 450, 50):
		obj = sp.request_springer(query, 'open', 50, config.springer_api_key, page)
		pprint.pprint(obj, raw_file)

		# strip irrelevant data, format and write to file
		sp.format_results(obj, paper_file)

	paper_file.close()
	raw_file.close()

''' generate_query()
This will format the provided information into a search query.

params: disease - a list containing the name(s) of the disease
		trait - a list containing the trait information
output: returns a string containing the query
'''
def generate_query(disease, trait):
	# add disease name(s). e.g. ("covid" OR "sars-cov-2")
	query = r'("'	
	query += r'" OR "'.join(disease)
	query += r'")'
	
	# use logical AND to link disease + trait info
	query += r' AND '
	
	# add trait information e.g.
	# ("proportion" OR "ratio" OR "rate") AND ("asymptomatic" OR "asymptomatic infection")
	
	
	print(query)	
	
	return query
	
	
''' get_disease_trait_data()
This function will read the files 'disease_list.txt' and 'trait_list.txt'
and format them into lists that are stored as global variables.
'''
def get_disease_trait_data():
	# Get the lists of diseases and traits
	disease_file = open(r'./search_parameters/disease_list.txt', 'r')
	trait_file = open(r'./search_parameters/trait_list.txt', 'r')
	
	# create a 2d list from disease_file of disease names
	# e.g. [[ebola],[covid-19,sars-cov-2,covid],[nipah]]
	for line in disease_file:
		# skip the instructions section in the header
		if line[0] == '*':
			continue
			
		# split by comma and add the names to diseases global var
		tmp = [word.rstrip('\n') for word in line.split(', ')]
		diseases.append(tmp)
		
	# create a multi-dimensional list from trait_file
	
	
	
	
	
	# close the files
	disease_file.close()
	trait_file.close()
	


''' Main '''
pp = pprint.PrettyPrinter(indent=1)

get_disease_trait_data()
print("Diseases:")
pp.pprint(diseases)
print()

for d in diseases:
	generate_query(d, [0])
	



'''
start = time.time()

end = time.time()
print("Run time was %d seconds" % (end-start))
'''


