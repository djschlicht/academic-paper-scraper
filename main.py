#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import config
import pprint
import time
import springer as sp

start = time.time()

# keywords relevant to disease traits
keywords = ['pathogenesis', 'incubation period', 'latent period', 
			'infectious period', 'origin', 'reservoir', 'outbreak',
			'host species']

# emerging disease pathogens 
pathogens = ['H1N1', 'Ebola', 'Zika', 'MERS', 'Chikungunya']

# create text files store the data
paper_file = open(r"./data/papers.txt", "w")
raw_file = open(r"./data/raw.txt", "w")

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

end = time.time()
print("Run time was %d seconds" % (end-start))
