#!/usr/bin/env python3
# This is the front-end of the academic journal scraper.

''' TODO:
[] fill out keywords and pathogens lists 
[] create modules for other publishers (ScienceDirect, etc)
[] format json results into a human-readable form
[] print list of articles/papers to a file
[] automate querying process
'''
import config
import pprint
from springer import request_springer

# keywords to search for - should be relevant to disease traits
keywords = ["pathogenesis", "incubation period"]

# a list of emerging disease pathogens 
pathogens = ['H1N1', 'SARS-CoV-2', 'Ebola']

# access Springer API to search for papers
# 	usage: request_springer(query, API type, max results)
# documentation to help form queries: https://dev.springernature.com/docs
obj = request_springer('(title:H1N1 AND "incubation period")', 'meta',
						10, config.springer_api_key)

pprint.pprint(obj)



