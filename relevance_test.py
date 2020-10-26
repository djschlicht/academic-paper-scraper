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
	
traits = [	# traits
	"first detected", "first recorded outbreak", "first outbreak", "outbreak",
	"geographic", "location", "origin", "human transmission",
	"asymptomatic", "incubation period", "infectious period", "latent period",
	"fatality rate", "mortality rate", "pre-symptomatic infection", "human-to-human",
	"animal-to-human", "vector", "reservoir", "host species",
	"interspecies transmission", "pathogenicity", "virulence"
	]

# deletes files that are empty or title only
def delete_if_empty(filename):
	size = os.path.getsize(f)
	
	# delete small files
	if size < 1000:
		print(f+' removed.')
		os.remove(f)
				

# returns hit count of words as a rough relevance test
def relevance_check(filename):
	count = 0	
	with open(filename, "r") as f:
		title = f.readline()
		for line in f:
			for elem in traits:
				if elem in line:
					count += 1
		
	return (title, count)


''' Main '''
# open a txt file to list relevance scores
rel_list = open(r"./relevance_list.txt", "w+")
relevances = {}
# iterate through the files and cleanup/run relevance test
for dirname in os.listdir(r"./data/springer/texts/"):
		for filename in os.listdir(r"./data/springer/texts/"+dirname):
			f = r"./data/springer/texts/"+dirname+"/"+filename
			delete_if_empty(f)
			title, rev = relevance_check(f)
			if rev in relevances:
				relevances[rev].append((title, f))
			else:
				relevances[rev] = [(title, f)]

# sort by hit count and write to file			
for k in sorted(relevances):
	rel_list.write((str(k)+": \n"))
	for tup in relevances[k]:
		rel_list.write("\t" + tup[0] + "\t\t" + tup[1] + "\n")
			
rel_list.close()
