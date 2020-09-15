#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

''' TODO:
[] fill out keywords and pathogens lists 
[] create modules for other publishers (ScienceDirect, etc)
[] automate querying process
'''
import config
import springer as sp

# should be relevant to disease traits
keywords = ["pathogenesis", "incubation period"]

# emerging disease pathogens 
pathogens = ['H1N1', 'SARS-CoV-2', 'Ebola']

# create a text file to list relevant papers
paper_file = open("papers.txt", "w")

# access Springer API to search for papers
# 	usage: request_springer(query, API type, max results)
# documentation to help form queries: https://dev.springernature.com/docs
obj = sp.request_springer('(H1N1 AND "incubation period")', 'meta',
						5, config.springer_api_key)

# strip irrelevant data, format and write to file
sp.format_results(obj, paper_file)

paper_file.close()
