# %%
#!/usr/bin/env python3
# main.py - the control script of the academic paper scraper

import pprint
import time
import springer as sp

# Put your own API key
springer_api_key = "e0b7d7365a763c1aa1a9cf2b518c2be4"

# %%
''' Functions ''' 
''' call_springer()
This function will put API calls into the Springer Database and store
the results in the files 'papers.txt' and 'raw.txt' in ./data/springer.
'''
def call_springer(query):
    # create text files to store the data
    paper_file = open(r"./data/springer/papers.txt", "w")
    raw_file = open(r"./data/springer/raw.txt", "w")

    # access Springer API to search for papers
    # 	usage: request_springer(query, API type, results per page, starting position)
    # documentation to help form queries: https://dev.springernature.com/docs
    for page in range(1, 450, 50):
        obj = sp.request_springer(query, 'open', 1, springer_api_key, page)
        pprint.pprint(obj, raw_file)

        # strip irrelevant data, format and write to file
        sp.format_results(obj, paper_file)

        paper_file.close()
        raw_file.close()


def get_keywords(file):
    keywords = []
    
    keyword_file = open(file, 'r')

    # parses through all lines
    for line in keyword_file:
        # skip the instructions section in the header
        if line[0] in ['*','\n']:
            continue
            
        # makes tuples out of OR groups
        line = line.strip("\n")
        print(line)
        keywords.append(tuple([x.strip() for x in line.split(',')]))
        
    keyword_file.close()
    
    return keywords

''' to_query()
This will format the provided information into a search query.

params: disease - a list containing the name(s) of the disease
    trait - a list containing the trait information
output: returns a string containing the query
'''
def to_query(keyword_group):
    query = ""
    if isinstance(keyword_group, tuple):
        query = r'("'	
        query += r'" OR "'.join(keyword_group)
        query += r'")'
    
    elif isinstance(keyword_group, list):
        formatted_keyword_tuples = [to_query(keyword_tuple) for keyword_tuple in keyword_group]
        query += r' AND '.join(formatted_keyword_tuples)

    return query

def concat_query(query1, query2):
    return query1 + " AND " + query2

# %%
''' Main '''
pp = pprint.PrettyPrinter(indent=1)

traits = get_keywords(r'./search_parameters/trait_list.txt')
diseases = get_keywords(r'./search_parameters/disease_list.txt')

trait_query = to_query(traits)

disease_query_list = []
for disease in diseases:
    disease_query_list.append(to_query(disease))

'''
start = time.time()

end = time.time()
print("Run time was %d seconds" % (end-start))
'''

# %%
trait_query

# %%
