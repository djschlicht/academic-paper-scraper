#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import config
import pprint
import time
import springer as sp

''' Search Keywords '''
keywords = ['pathogenesis', 'incubation period', 'latent period', 
			'infectious period', 'origin', 'reservoir', 'outbreak',
			'host species']
pathogens = ['H1N1', 'Ebola', 'Zika', 'MERS', 'Chikungunya']

''' Functions '''
# get sources from springer (nature)
def mine_springer():
	# create text files to store the data
	paper_file = open(r"./data/springer/papers.txt", "w")
	raw_file = open(r"./data/springer/raw.txt", "w")

	# generate the query to use
	query = sp.generate_query(keywords, pathogens)

	# access Springer API to search for papers
	# 	usage: request_springer(query, API type, results per page, starting position)
	# documentation to help form queries: https://dev.springernature.com/docs
	for page in range(1, 450, 50):
		obj = sp.request_springer(query, 'meta', 50, config.springer_api_key, page)
		pprint.pprint(obj, raw_file)

		# strip irrelevant data, format and write to file
		sp.format_results(obj, paper_file)

	paper_file.close()
	raw_file.close()

# get sources from elsevier (sciencedirect)
def mine_elsevier():
	# create files
	raw_file = open(r"./data/elsevier/raw.txt", "w")
	
	raw_file.close()


'''
start = time.time()

end = time.time()
print("Run time was %d seconds" % (end-start))
'''


