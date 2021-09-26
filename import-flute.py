#!/usr/bin/env python

"""
  Script to import data from .csv file to Model Database DJango
  To execute this script run: 
                              1) manage.py shell
                              2) exec(open('import-flute.py').read())
"""

import csv
from Piece.models import Composer, Location, Piece, InstrumentGroup, Instrument, Category, Publisher

CSV_PATH = './import-flute.csv'

with open(CSV_PATH, newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    # Model.objects.create(... Attributes here ...)
    # Example -> Book.objects.create(ISBNCode=row[0], title=row[1], author=row[2])
    instrument = Instrument.objects.get(name=row[2])
    if instrument == None:
      instrument = Instrument.objects.create(name=row[2], abbreviation=row[2][0:2].upper())
    

