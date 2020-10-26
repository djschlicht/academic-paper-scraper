#!/usr/bin/env python3
# relevance_test.py - uses bag of words to assign a relevance score to 
# full texts

import os

# get words for bag from disease and trait files
diseases = [ # diseases
	"ebola", "EVD", "zika", "ZIKV", "nipah","NiV","chikungunya", "CHIKV", "hendra",
	"marburg", "MVD", "MARV", "dengue", "DENV", "lassa", "Lujo", "Lusaka/Johannesburg",
	"Lyme disease", "Lyme borreliosis","West nile", "heartland virus", "HRTV", 
	"Severe fever with thrombocytopenia syndrome", "SFTS", "St. Louis virus",
	"Powassan virus", "POWV", "deer tick virus", "DTV", "Australian bat lyssavirus",
	"ABLV", "H1N1", "swine flu", "pig flu", "MERS", "middle east respiratory syndrome",
	"avian flu", "bird flu", "avian influenza", "HIV", "human immunodeficiency virus",
	"SARS", "SARS-COV", "severe acute respiratory syndrome", "Covid", "SARS-COV-2", "novel coronavirus",
	]
	
traits=[	# traits
	"first detected", "first recorded outbreak", "first outbreak", "outbreak",
	"geographic", "location", "origin", "human transmission",
	"asymptomatic", "incubation period", "infectious period", "latent period",
	"fatality rate", "mortality rate", "pre-symptomatic infection", "human-to-human",
	"animal-to-human", "vector", "reservoir", "host species",
	"interspecies transmission", "pathogenicity", "virulence"
	]

# deletes files that are empty or title only
def cleanup_files():
	print("Removing empty files")
	for dirname in os.listdir(r"./data/springer/texts/"):
		for filename in os.listdir(r"./data/springer/texts/"+dirname):
			f = r"./data/springer/texts/"+dirname+"/"+filename
			size = os.path.getsize(f)
			
			# delete small files
			if size < 1000:
				print(f+' removed.')
				os.remove(f)
				

# runs bag-o-words and returns hit count
def relevance_check(filename):
	count = 0
	
	
	
	for elem in bag:
		if elem in line:
			count += 1
	
	return count



cleanup_files()
