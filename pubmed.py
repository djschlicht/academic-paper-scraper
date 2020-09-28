#!/usr/bin/env python3


import config
from pymed import PubMed

pubmed = PubMed(tool="academic-paper-scraper", email=config.pubmed_email)
