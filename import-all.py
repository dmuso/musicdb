#!/usr/bin/env python

"""
  Script to import data from .csv file to Model Database DJango
  To execute this script run: 
    1) docker-compose run app python manage.py shell < import-all.py
"""

import csv
import datetime
from piece.models import Composer, Arranger, Location, Piece, InstrumentGroup, Instrument, Category, Publisher, Grade, EnsemblePart, Genre, Status

CSV_PATH = './import-all.csv'

Piece.objects.all().delete()
Category.objects.all().delete()
Publisher.objects.all().delete()
Location.objects.all().delete()
Composer.objects.all().delete()
Arranger.objects.all().delete()
Grade.objects.all().delete()
Genre.objects.all().delete()
Status.objects.all().delete()
EnsemblePart.objects.all().delete()
Instrument.objects.all().delete()
InstrumentGroup.objects.all().delete()

category_unknown = Category.objects.create(name="Unknown", code="XX")
publisher_unknown = Publisher.objects.create(name="Unknown")
location_unknown = Location.objects.create(name="Unknown")
print(f"Created unknown category, publisher, location")

with open(CSV_PATH, newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:

    catalogue_number = row[0].strip().lstrip()
    print(f"Catalogue Number: {catalogue_number}")
    
    title = row[8].strip().lstrip()
    if title == "":
      title = "<Unknown>"
    print(f"Title: {title}")

    instrument_field = row[2].strip().lstrip()
    instrument_group_field = row[3].strip().lstrip()
    instruments = Instrument.parse_str_instruments(instruments=instrument_field)
    print(f"Parsed Instruments: {instruments}")
    try:
      instrument_group = InstrumentGroup.objects.get(name=instrument_group_field)
      print(f"Found Instrument Group: name={instrument_group}")
    except InstrumentGroup.DoesNotExist:
      instrument_group = InstrumentGroup.objects.create(name=instrument_group_field)
      print(f"Create Instrument Group: name={instrument_group}")
    for instrument in instruments:
      instrument.instrument_group = instrument_group
      print(f"Instrument '{instrument}' has been given Instrument Group '{instrument_group}'")
      instrument.save()
      print(f"Saved Instrument name={instrument}")

    category_field = row[4].strip().lstrip()
    categories = Category.parse_str_categories(categories=category_field)
    print(f"Parsed Categories: {categories}")
    for category in categories:
      category.save()
      print(f"Saved Category name={category}")

    publisher_field = row[12].strip().lstrip()
    publisher = None
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

    location_field = row[29].strip().lstrip()
    location = None
    try:
      location = Location.objects.get(name=location_field)
      print(f"Found Location: name={location}")
    except Location.DoesNotExist:
      if location_field == "":
        location = location_unknown
        print(f"Location Unknown.")
      else:
        location = Location.objects.create(name=location_field)
        print(f"Create Location: name={location_field}")

    status_field = row[30].strip().lstrip()
    status = None
    if status_field != "":
      try:
        status = Status.objects.get(name=status_field)
        print(f"Found Status: name={status}")
      except Status.DoesNotExist:
        status = Status.objects.create(name=status_field)
        print(f"Create Status: name={status_field}")
    else:
      print(f"Status is blank.")

    composer_field = row[9].strip().lstrip()
    composers = Composer.parse_str_composers(composers=composer_field)
    print(f"Parsed composers: {composers}")
    for composer in composers:
      composer.save()
      print(f"Saved Composer name={composer}")

    arranger_field = row[10].strip().lstrip()
    arrangers = Arranger.parse_str_arrangers(arrangers=arranger_field)
    print(f"Parsed arrangers: {arrangers}")
    for arranger in arrangers:
      arranger.save()
      print(f"Saved Arranger name={arranger}")

    ensemble_parts_field = row[7].strip().lstrip()
    ensemble_parts = []
    if ensemble_parts_field != "":
      ensemble_parts = EnsemblePart.parse_str_ensemble_parts(ensemble_parts=ensemble_parts_field)
      print(f"Parsed ensemble_parts: {ensemble_parts}")
      for ep in ensemble_parts:
        ep.save()
        print(f"Saved EnsemblePart name={ep}")
    else:
      print(f"EnsemblePart is blank.")
    
    accompaniment_field = row[18].strip().lstrip()
    accompaniments = []
    accompaniment_note = ""
    if accompaniment_field != "":
      accompaniment_note = accompaniment_field
      accompaniments = Instrument.parse_str_accompaniments(instruments=accompaniment_field)
      print(f"Parsed Accompaniments: {accompaniments}")
      if len(accompaniments) < 1:
        print(f"Accompaniment was not blank but no accompaniment match found for {accompaniment_field}")
    else:
      print("Accompaniment is Blank.")

    soloists_field = row[16].strip().lstrip()
    soloists = []
    if soloists_field != "":
      soloists = Instrument.parse_str_accompaniments(instruments=soloists_field)
      print(f"Parsed Solists: {soloists}")
      if len(soloists) < 1:
        print(f"Soloist was not blank but no accompaniment match found for {soloists_field}")
    else:
      print("Soloist is Blank.")

    number_of_originals = row[14].strip().lstrip()
    if number_of_originals == "":
      number_of_originals = 1
    print(f"Number of Originals: {number_of_originals}")

    number_of_copies = row[15].strip().lstrip()
    if number_of_copies == "":
      number_of_copies = 1
    print(f"Number of Copies: {number_of_copies}")

    grade_field = row[5].strip().lstrip()
    grades = []
    if grade_field != "":
      grades = Grade.parse_str_grades(grades=grade_field)
      print(f"Parsed grades: {grades}")
      for grade in grades:
        grade.save()
        print(f"Saved Grade name={grade}")

    grade_field = row[19].strip().lstrip()
    if grade_field != "":
      grades_other = Grade.parse_str_grades(grades=grade_field)
      print(f"Parsed grades: {grades_other}")
      for grade in grades_other:
        grade.save()
        grades.append(grade)
        print(f"Saved Grade name={grade}")

    movements = row[20].strip().lstrip()
    if movements == "":
      movements = None
    print(f"Movements: {movements}")

    performance_time = row[21].strip().lstrip()
    if performance_time == "":
      performance_time = None
    print(f"Performance time: {performance_time}")

    genre_field = row[22].strip().lstrip()
    genre = None
    if genre_field != "":
      try:
        genre = Genre.objects.get(name=genre_field)
        print(f"Found Genre: name={genre}")
      except Genre.DoesNotExist:
        genre = Genre.objects.create(name=genre_field)
        print(f"Create Location: name={genre_field}")

    medley_field = row[23].strip().lstrip()
    if medley_field == "" or medley_field == "N" or medley_field == "No":
      medley = False
    else:
      medley = True
    print(f"Medley: {medley}")

    arrangement = row[6].strip().lstrip()
    print(f"Arrangement: {arrangement}")

    isbn = row[13].strip().lstrip()
    print(f"ISBN: {isbn}")

    sacred_field = row[17].strip().lstrip()
    if sacred_field == "" or sacred_field == "NS":
      sacred = False
    else:
      sacred = True
    print(f"Sacred: {sacred}")

    missing_parts = row[24].strip().lstrip()
    print(f"Missing Parts: {missing_parts}")

    related_file = row[25].strip().lstrip()
    print(f"Related File: {related_file}")

    year_purchased = row[26].strip().lstrip()
    if year_purchased == "":
      year_purchased = None
    print(f"Year Purchased: {year_purchased}")

    year_last_performed = row[27].strip().lstrip()
    if year_last_performed == "":
      year_last_performed = None
    print(f"Year Last Performed: {year_last_performed}")

    date_last_checked_field = row[28].strip().lstrip()
    if date_last_checked_field == "":
      date_last_checked = datetime.date(1900, 1, 1)
    else:
      date_parts = date_last_checked_field.split("/")
      date_last_checked = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
      print(f"Date Last Checked: {date_last_checked}")

    song_list = row[31].strip().lstrip()
    print(f"Song List: {song_list}")

    notes = row[32].strip().lstrip()
    print(f"Notes: {notes}")

    print(f"Starting Piece creation...")
    try:
      piece = Piece.objects.get(title=title, catalogue_number=catalogue_number)
      print(f"   Piece skipped - found: {piece.pk}")
    except Piece.DoesNotExist:
      piece = Piece(
        publisher=publisher,
        location=location,
        catalogue_number=catalogue_number,
        number_of_copies=number_of_copies,
        number_of_originals=number_of_originals,
        title=title,
        isbn=isbn,
        missing_parts=missing_parts,
        date_last_checked=date_last_checked,
        notes=notes,
        accompaniment_note=accompaniment_note,
        sacred=sacred,
        movements=movements,
        performance_time=performance_time,
        genre=genre,
        medley=medley,
        related_file=related_file,
        year_purchased=year_purchased,
        year_last_performed=year_last_performed,
        status=status,
        song_list=song_list,
        )
      piece.save()
      print(f"   Piece instruments: {instruments}")
      for i in instruments:
        piece.instruments.add(i)
      print(f"   Piece categories: {categories}")
      for cat in categories:
        piece.categories.add(cat)
      print(f"   Piece composers: {composers}")
      for c in composers:
        piece.composers.add(c)
      print(f"   Piece arrangers: {arrangers}")
      for arr in arrangers:
        piece.arrangers.add(arr)
      print(f"   Piece accompaniments: {accompaniments}")
      for a in accompaniments:
        piece.accompaniment.add(a)
      print(f"   Piece grades: {grades}")
      for g in grades:
        piece.grades.add(g)
      print(f"   Piece ensemble parts: {ensemble_parts}")
      for e in ensemble_parts:
        piece.ensemble_parts.add(e)
      print(f"   Piece soloists: {soloists}")
      for s in soloists:
        piece.soloists.add(s)
      print(f"Piece created: {piece.pk}")

    print("-----")
