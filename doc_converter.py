#!/usr/bin/env python3
# doc_converter.py

import PyPDF2
import requests
import os

'''get_pdf
downloads pdf from url
Params: the url of the pdf
returns: filepath from current dir to downloaded pdf
'''
def get_pdf(url):
	r = requests.get(url)
	
	# just put it in a jumk folder in texts because we delete anyway
	fp = './texts/tmp_pdf/tmp.pdf' 
	with open(fp, 'wb') as f:
		f.write(r.content)
		
	return fp
	
'''pdf_to_text
converts a pdf into easily mineable text file
params: doi, so you can name the text file created and organize it
		pdf_path, the path to the pdf file to convert
returns: path to the newly created text file
'''
def pdf_to_text(pdf_path, doi):	
	'''
	name text file according to this convention:
		-split doi along slash
		-create folder name with left side
		-create file name with right side
		-place file in folder
		-full doi can be easily obtained by combining them
	'''
	names = doi.split('/')
	folder_name = names[0]
	txt_name = names[1]
	
	# make directory with folder_name where you store full texts
	# first check if the dir already exists
	txt_path = './texts/'+folder_name+'/'
	if os.path.exists(txt_path):
		raise Exception("Error: That filepath already exists.")
	else:
		os.mkdir(txt_path)
	
	# add file name to the path
	txt_path += txt_name+'.txt'
	
	# open the pdf and write to the file you just named
	with open(pdf_path, 'rb') as pdf_file, open(txt_path, 'w') as txt_file:
		# spool up a reader
		reader = PyPDF2.PdfFileReader(pdf_file)
		# get number of pages
		num_pages = reader.numPages
		# loop to get text from all pages and write to txt file
		for num in range(num_pages):
			page = reader.getPage(num)
			page_content = page.extractText()
			txt_file.write(page_content)
	
	return txt_path
			
''' get_text
Controller function for this script. Fits the pieces together and is 
accessed through main.py.
params: doi of document being downloaded and converted
return: file path of newly converted text file
'''
def get_text(doi):
	# craft url to send to get_pdf() 
	# will change for non-springer stuff but we can adapt it 
	url = 'https://link.springer.com/content/pdf/' + doi + '.pdf'
	
	# get the pdf
	pdf_path = get_pdf(url)
	
	# convert it to a text file
	txt_path = pdf_to_text(pdf_path, doi)
	
	# clear out the pdf to save space
	if os.path.exists(pdf_path):
		os.remove(pdf_path)
	
	# return path to text file
	return txt_path
