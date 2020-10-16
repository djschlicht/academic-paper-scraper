#!/usr/bin/env python3
# text_scraper.py - scrapes websites for the full text of an article

import pprint
import requests
import re
from bs4 import BeautifulSoup
# beautifulsoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

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
			
	# get abstract
	abstract_title = soup.find('h2', id=re.compile('^Abs[0-9]{1,2}$'))
	abstract_content = soup.find('div', id=re.compile('^Abs[0-9]{1,2}-content'))
		
	# get rest of section titles + contents
	section_titles = soup.find_all('h2', id=re.compile('^Sec[0-9]{1,2}$'))
	section_contents = soup.find_all('div', id=re.compile('^Sec[0-9]{1,2}-content$'))

	# add everything into a string
	full_text = ''
	if title != None:
		full_text += title.get_text() + '\n\n' 
	if abstract_title != None:
		full_text += abstract_title.get_text() + '\n' 
	if abstract_content != None:
		full_text += abstract_content.get_text() + '\n'
		
	num_sections = len(section_titles)
	for s in range(num_sections):
		if section_titles[s] != None:
			full_text += '\n' + section_titles[s].get_text() + '\n' 
		if section_contents[s] != None:
			full_text += section_contents[s].get_text() + '\n'		
					
	return full_text

''' get_fulltext 
Controller function for this script
Params: url, the url to be scraped as a string
Returns: a string containing the text of the paper
'''
def get_fulltext(url):
	r = requests.get(url)	
	text = filter_html(r)
	
	return text
