#!/usr/bin/env python

"""
  Script to import data from .csv file to Model Database DJango
  To execute this script run: 
                              1) manage.py shell
                              2) exec(open('import-flute.py').read())
"""

import csv
import datetime
from piece.models import Composer, Location, Piece, InstrumentGroup, Instrument, Category, Publisher

CSV_PATH = './import-flute.csv'

with open(CSV_PATH, newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    instrument_group_unknown = InstrumentGroup.objects.get(name="Unknown")
    category_unknown = Category.objects.get(name="Unknown")
    publisher_unknown = Publisher.objects.get(name="Unknown")

    try:
      instrument = Instrument.objects.get(name=row[2])
      print(f"Found Instrument: name={instrument}")
    except Instrument.DoesNotExist:
      instrument = Instrument.objects.create(name=row[2], abbreviation=row[2][0:2].upper(), instrument_group=instrument_group_unknown)
      print(f"Create Instrument: name={row[2]}, abbreviation={row[2][0:2].upper()}, instrument_group={instrument_group_unknown}")

    category_field = row[3].strip()
    try:
      category = Category.objects.get(code=category_field[1:3])
      print(f"Found Category: name={category}")
    except Category.DoesNotExist:
      if category_field == "":
        category = category_unknown
        print(f"Category Unknown.")
      else:
        category = Category.objects.create(name=category_field, code=category_field[1:3])
        print(f"Create Category: name={category_field}, code={category_field[1:3]}")

    publisher_field = row[8].strip()
    try:
      publisher = Publisher.objects.get(name=publisher_field)
      print(f"Found Publisher: name={publisher}")
    except Publisher.DoesNotExist:
      if publisher_field == "":
        publisher = publisher_unknown
        print(f"Publisher Unknown.")
      else:
        publisher = Publisher.objects.create(name=publisher_field)
        print(f"Create Publisher: name={publisher_field}")

    location_field = row[11].strip()
    try:
      location = Location.objects.get(name=location_field)
      print(f"Found Location: name={location}")
    except Location.DoesNotExist:
      if location_field == "":
        location = Location.objects.create(name="Unknown", code="XX")
        print(f"Create Location: name='Unknown', code='XX'")
      else:
        location = Location.objects.create(name=location_field)
        print(f"Create Location: name={location_field}")

    composer_field = row[7].strip()
    composer_fields = composer_field.split("/")
    composers = []
    for composer_raw in composer_fields:
      composer_raw = composer_raw.strip()
      composer_names = composer_raw.split(",")
      composer_last_name = composer_names[0].strip()
      if len(composer_names) > 1:
        composer_first_name = composer_names[1].strip()
      else:
        composer_first_name = "."
      try:
        composer = Composer.objects.get(first_name=composer_first_name, last_name=composer_last_name)
        print(f"Found Composer: name={composer}")
      except Composer.DoesNotExist:
        if composer_field == "":
          composer = Composer.objects.create(first_name="Unknown", last_name="Composer")
          print(f"Create Composer: first_name='Unknown', last_name='Composer'")
        else:
          composer = Composer.objects.create(first_name=composer_first_name, last_name=composer_last_name)
          print(f"Create Composer: first_name={composer_first_name}, last_name={composer_last_name}")
      composers.append(composer)
    
    accompaniment_field = row[6].strip()
    accompaniments = []
    if accompaniment_field != "":
      accompaniment_fields = accompaniment_field.split(",")
      for accompaniment_name in accompaniment_fields:
        accompaniment_name = accompaniment_name.strip()
        try:
          accompaniment = Instrument.objects.get(name__iexact=accompaniment_name)
          print(f"Found Accompaniment: name={accompaniment}")
        except Instrument.DoesNotExist:
          accompaniment = Instrument.objects.create(name=accompaniment_name, abbreviation=accompaniment_name[0:2].upper(), instrument_group=instrument_group_unknown)
          print(f"Create Accompaniment: name={accompaniment_name}, abbreviation={accompaniment_name[0:2].upper()}, instrument_group={instrument_group_unknown}")
        accompaniments.append(accompaniment)
    else:
      print("Accompaniment is Blank.")

    catalogue_number = row[0].strip()
    if catalogue_number == "":
      catalogue_number = "N/A"
    print(f"Catalogue Number: {catalogue_number}")
    
    number_of_copies = row[1].strip()
    if number_of_copies == "":
      number_of_copies = 1
    print(f"Number of Copies: {number_of_copies}")

    title = row[5].strip()
    if title == "":
      title = "Blank"
    print(f"Title: {title}")

    grade = row[4].strip()
    print(f"Grade: {grade}")

    isbn = row[9].strip()
    print(f"ISBN: {isbn}")

    missing_parts = row[10].strip()
    print(f"Missing Parts: {missing_parts}")

    date_last_checked_field = row[12].strip()
    if date_last_checked_field == "":
      date_last_checked = datetime.date(1900, 1, 1)
    else:
      date_parts = date_last_checked_field.split("/")
      date_last_checked = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
      print(f"Date Last Checked: {date_last_checked}")

    notes = row[13].strip()
    print(f"Notes: {notes}")

    try:    
      piece = Piece.objects.get(title=title, catalogue_number=catalogue_number)
      print(f"Piece skipped - found: {piece.pk}")
    except Piece.DoesNotExist:
      piece = Piece(
        instrument=instrument,
        category=category,
        publisher=publisher,
        location=location,
        catalogue_number=catalogue_number,
        number_of_copies=number_of_copies,
        title=title,
        grade=grade,
        isbn=isbn,
        missing_parts=missing_parts,
        date_last_checked=date_last_checked,
        notes=notes
        )
      piece.save()
      for c in composers:
        piece.composers.add(c)
      for a in accompaniments:
        piece.accompaniment.add(a)
      print(f"Piece created: {piece.pk}")

    print("-----")