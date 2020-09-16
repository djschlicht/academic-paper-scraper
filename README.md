# academic-paper-scraper

## Summary
The purpose of academic-paper-scraper is to automate data collection from
academic databases. Our use case is to gather sources of information regarding the traits
of emerging infectious pathogens, such as SARS-CoV-2 and Zika, but it 
can be easily adapted for other research goals. It current uses the 
Springer APIs to search for articles, but functionality for the Elsevier 
APIs is in progress.

## How To
### Set Up
* Request an API key from [Springer](https://dev.springernature.com/)
* Clone this repository
* Create a config.py file and put your API key in it
* To run it type `python3 main.py` while in the folder of your cloned repository
* Results will go into a folder called data/ in your current working directory
### Modify
* Change the bounds of the for loop in main.py to get more or fewer results
* Add your own items to the lists `keywords` and `pathogens`
* Modify the `query_generator` function in springer.py. Springer's API
[documentation](https://dev.springernature.com/docs) can help with that

## Technology
This is written purely in Python3 and uses the `requests` library for API calls.

## To Do
* expand lists of trait-keywords and emerging pathogens
* refine query generation
* add modules for other academic publishers
