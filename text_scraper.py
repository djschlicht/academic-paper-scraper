#!/usr/bin/env python3
# text_scraper.py - scrapes websites for the full text of an article

import pprint
import requests
import re
from bs4 import BeautifulSoup

''' filter_html
Params: site, a response object that contains a websites information
returns: the filtered html containing the actual paper
'''
def filter_html(site):
	
	# string to store html elements of paper
	paper_html = ''
	
	# use bs4 to parse the html
	soup = BeautifulSoup(site.content, 'html.parser')

	# get article title
	title = soup.find(class_='c-article-title')

	# get html section containing the article
	body = soup.find(class_='c-article-body')		
			
	# get abstract
	abstract_title = body.find('h2', id=re.compile('^Abs[0-9]{1,2}$'))
	abstract_content = body.find('div', id=re.compile('^Abs[0-9]{1,2}-content'))
		
	# get rest of section titles + contents
	section_titles = body.find_all('h2', id=re.compile('^Sec[0-9]{1,2}$'))
	section_contents = body.find_all('div', id=re.compile('^Sec[0-9]{1,2}-content$'))

	# add everything into a string
	full_text = title.string + '\n\n' + abstract_title.string + '\n' + \
		abstract_content.get_text() + '\n'
	num_sections = len(section_titles)
	for s in range(num_sections):
		full_text += '\n' + section_titles[s].string + '\n' + \
			section_contents[s].get_text() + '\n'		
					
	return full_text

''' get_fulltext 
Controller function for this script
Params: url, the url to be scraped as a string
Returns: a string containing the text of the paper
'''
def get_fulltext(url):
	r = requests.get(url)	
	text = filter_html(r)
	doi = url.lstrip('http://dx.doi.org/')
	text += '\nDOI: ' + doi
	
	return text
	return text
