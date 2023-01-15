#!/usr/bin/env python

"""
  Script to import data from .csv file to Model Database DJango
  To execute this script run: 
    1) docker-compose run app python manage.py shell < import-all.py
"""

import csv
import datetime
from piece.models import Composer, Arranger, Location, Piece, InstrumentGroup, Instrument, ShelfLocation, Publisher, Grade, EnsemblePart, Genre, Status

CSV_PATH = './import-all.csv'

COL = {
  'CATALOGUE_NUMBER': 0,
  'SHORT_NO': 1,
  'INSTRUMENT_GROUP': 2,
  'INSTRUMENT': 3,
  'SHELF_LOCATION': 4,
  'VOLUME_NO': 5,
  'VOCAL_ARRANGEMENT': 6,
  'ENSEMBLE_PARTS': 7,
  'TITLE': 8,
  'COMPOSER': 9,
  'ARRANGER': 10,
  'PUBLISHER': 12,
  'ISBN': 13,
  'NO_ORIGINALS': 14,
  'NO_COPIES': 15,
  'SOLOIST': 16,
  'SACRED': 17,
  'ACCOMPANIMENT': 18,
  'GRADE': 19,
  'NO_MOVEMENTS': 20,
  'PERFORMANCE_TIME': 21,
  'GENRE': 22,
  'MEDLEY': 23,
  'MISSING_PARTS': 24,
  'RELATED_FILE': 25,
  'YEAR_PURCHASED': 26,
  'YEARS_PERFORMED': 27,
  'DATE_LAST_CHECKED': 28,
  'LOCATION': 29,
  'STATUS': 30,
  'SONG_LIST': 31,
  'NOTES': 32,
}

Piece.objects.all().delete()
ShelfLocation.objects.all().delete()
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

shelf_location_unknown = ShelfLocation.objects.create(name="Unknown", code="XX")
publisher_unknown = Publisher.objects.create(name="Unknown")
location_unknown = Location.objects.create(name="Unknown")
print(f"Created unknown shelf_location, publisher, location")

with open(CSV_PATH, newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:

    catalogue_number = row[COL['CATALOGUE_NUMBER']].strip().lstrip()
    print(f"Catalogue Number: {catalogue_number}")
    
    title = row[COL['TITLE']].strip().lstrip()
    if title == "":
      title = "<Unknown>"
    print(f"Title: {title}")

    instrument_field = row[COL['INSTRUMENT']].strip().lstrip()
    instrument_group_field = row[COL['INSTRUMENT_GROUP']].strip().lstrip()
    instruments = Instrument.parse_str_instruments(instruments=instrument_field)
    print(f"Parsed Instruments: {instruments}")
    try:
      instrument_group = InstrumentGroup.objects.get(name__iexact=instrument_group_field.lower())
      print(f"Found Instrument Group: name={instrument_group}")
    except InstrumentGroup.DoesNotExist:
      instrument_group = InstrumentGroup.objects.create(name=instrument_group_field)
      print(f"Create Instrument Group: name={instrument_group}")
    for instrument in instruments:
      instrument.instrument_group = instrument_group
      print(f"Instrument '{instrument}' has been given Instrument Group '{instrument_group}'")
      instrument.save()
      print(f"Saved Instrument name={instrument}")

    shelf_location_field = row[COL['SHELF_LOCATION']].strip().lstrip()
    shelf_locations = ShelfLocation.parse_str_shelf_locations(shelf_locations=shelf_location_field)
    print(f"Parsed ShelfLocations: {shelf_locations}")
    for shelf_location in shelf_locations:
      shelf_location.save()
      print(f"Saved ShelfLocation name={shelf_location}")

    publisher_field = row[COL['PUBLISHER']].strip().lstrip()
    publisher = None
    try:
      publisher = Publisher.objects.get(name__iexact=publisher_field.lower())
      print(f"Found Publisher: name={publisher}")
    except Publisher.DoesNotExist:
      if publisher_field == "":
        publisher = publisher_unknown
        print(f"Publisher Unknown.")
      else:
        publisher = Publisher.objects.create(name=publisher_field)
        print(f"Create Publisher: name={publisher_field}")

    location_field = row[COL['LOCATION']].strip().lstrip()
    locations = Location.parse_str_locations(locations=location_field)
    print(f"Parsed locations: {locations}")
    for location in locations:
      location.save()
      print(f"Saved Location name={location}")

    status_field = row[COL['STATUS']].strip().lstrip()
    status = None
    if status_field != "":
      try:
        status = Status.objects.get(name__iexact=status_field.lower())
        print(f"Found Status: name={status}")
      except Status.DoesNotExist:
        status = Status.objects.create(name=status_field)
        print(f"Create Status: name={status_field}")
    else:
      print(f"Status is blank.")

    composer_field = row[COL['COMPOSER']].strip().lstrip()
    composers = Composer.parse_str_composers(composers=composer_field)
    print(f"Parsed composers: {composers}")
    for composer in composers:
      composer.save()
      print(f"Saved Composer name={composer}")

    arranger_field = row[COL['ARRANGER']].strip().lstrip()
    arrangers = Arranger.parse_str_arrangers(arrangers=arranger_field)
    print(f"Parsed arrangers: {arrangers}")
    for arranger in arrangers:
      arranger.save()
      print(f"Saved Arranger name={arranger}")

    ensemble_parts_field = row[COL['ENSEMBLE_PARTS']].strip().lstrip()
    ensemble_parts = []
    if ensemble_parts_field != "":
      ensemble_parts = EnsemblePart.parse_str_ensemble_parts(ensemble_parts=ensemble_parts_field)
      print(f"Parsed ensemble_parts: {ensemble_parts}")
      for ep in ensemble_parts:
        ep.save()
        print(f"Saved EnsemblePart name={ep}")
    else:
      print(f"EnsemblePart is blank.")
    
    accompaniment_field = row[COL['ACCOMPANIMENT']].strip().lstrip()
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

    soloists_field = row[COL['SOLOIST']].strip().lstrip()
    soloists = []
    if soloists_field != "":
      soloists = Instrument.parse_str_accompaniments(instruments=soloists_field)
      print(f"Parsed Solists: {soloists}")
      if len(soloists) < 1:
        print(f"Soloist was not blank but no accompaniment match found for {soloists_field}")
    else:
      print("Soloist is Blank.")

    number_of_originals = row[COL['NO_ORIGINALS']].strip().lstrip()
    if number_of_originals == "":
      number_of_originals = 1
    print(f"Number of Originals: {number_of_originals}")

    number_of_copies = row[COL['NO_COPIES']].strip().lstrip()
    if number_of_copies == "":
      number_of_copies = 1
    print(f"Number of Copies: {number_of_copies}")

    grade_field = row[COL['VOLUME_NO']].strip().lstrip()
    grades = []
    if grade_field != "":
      grades = Grade.parse_str_grades(grades=grade_field)
      print(f"Parsed grades: {grades}")
      for grade in grades:
        grade.save()
        print(f"Saved Grade name={grade}")

    grade_field = row[COL['GRADE']].strip().lstrip()
    if grade_field != "":
      grades_other = Grade.parse_str_grades(grades=grade_field)
      print(f"Parsed grades: {grades_other}")
      for grade in grades_other:
        grade.save()
        grades.append(grade)
        print(f"Saved Grade name={grade}")

    movements = row[COL['NO_MOVEMENTS']].strip().lstrip()
    if movements == "":
      movements = None
    print(f"Movements: {movements}")

    performance_time = row[COL['PERFORMANCE_TIME']].strip().lstrip()
    if performance_time == "":
      performance_time = None
    print(f"Performance time: {performance_time}")

    genres_field = row[COL['GENRE']].strip().lstrip()
    genres = []
    if genres_field != "":
      genres = Genre.parse_str_genres(genres=genres_field)
      print(f"Parsed genres: {genres}")
      for g in genres:
        g.save()
        print(f"Saved Genre name={g}")
    else:
      print(f"Genre is blank.")

    medley_field = row[COL['MEDLEY']].strip().lstrip()
    if medley_field == "" or medley_field == "N" or medley_field == "No":
      medley = False
    else:
      medley = True
    print(f"Medley: {medley}")

    arrangement = row[COL['VOCAL_ARRANGEMENT']].strip().lstrip()
    print(f"Arrangement: {arrangement}")

    isbn = row[COL['ISBN']].strip().lstrip()
    print(f"ISBN: {isbn}")

    sacred_field = row[COL['SACRED']].strip().lstrip()
    if sacred_field == "" or sacred_field == "NS":
      sacred = False
    else:
      sacred = True
    print(f"Sacred: {sacred}")

    missing_parts = row[COL['MISSING_PARTS']].strip().lstrip()
    print(f"Missing Parts: {missing_parts}")

    related_file = row[COL['RELATED_FILE']].strip().lstrip()
    print(f"Related File: {related_file}")

    year_purchased = row[COL['YEAR_PURCHASED']].strip().lstrip()
    if year_purchased == "":
      year_purchased = None
    print(f"Year Purchased: {year_purchased}")

    year_last_performed = row[COL['YEARS_PERFORMED']].strip().lstrip()
    if year_last_performed == "":
      year_last_performed = None
    print(f"Year Last Performed: {year_last_performed}")

    date_last_checked_field = row[COL['DATE_LAST_CHECKED']].strip().lstrip()
    if date_last_checked_field == "":
      date_last_checked = datetime.date(1900, 1, 1)
    else:
      date_parts = date_last_checked_field.split("/")
      date_last_checked = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
      print(f"Date Last Checked: {date_last_checked}")

    song_list = row[COL['SONG_LIST']].strip().lstrip()
    print(f"Song List: {song_list}")

    notes = row[COL['NOTES']].strip().lstrip()
    print(f"Notes: {notes}")

    print(f"Starting Piece creation...")
    try:
      piece = Piece.objects.get(title=title, catalogue_number=catalogue_number)
      print(f"   Piece skipped - found: {piece.pk}")
    except Piece.DoesNotExist:
      piece = Piece(
        publisher=publisher,
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
      print(f"   Piece locations: {locations}")
      for loc in locations:
        piece.locations.add(loc)
      print(f"   Piece shelf_locations: {shelf_locations}")
      for cat in shelf_locations:
        piece.shelf_locations.add(cat)
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
      print(f"   Piece genres: {genres}")
      for g in genres:
        piece.genres.add(g)
      print(f"   Piece soloists: {soloists}")
      for s in soloists:
        piece.soloists.add(s)
      print(f"Piece created: {piece.pk}")

    print("-----")
