#!/usr/bin/env python3
# db.py - create the database in csv format and populate it with information

import pandas

df = pandas.read_csv('db.csv')
print(df)
