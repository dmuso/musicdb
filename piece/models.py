from os import stat
from django.db import models
from django.db.models.deletion import PROTECT
import re
# from django.db.models import UniqueConstraint

# ---

class InstrumentGroup(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  # UniqueConstraint(fields=['name'], name='unique_instrument_name')
  # UniqueConstraint(fields=['abbreviation'], name='unique_instrument_abbreviation')

# ---

class Instrument(models.Model):
  instrument_group = models.ForeignKey(InstrumentGroup, on_delete=PROTECT)
  name = models.CharField(max_length=240)
  abbreviation = models.CharField(max_length=2)

  class Meta:
    ordering = ['instrument_group', 'name']

  def __str__(self) -> str:
    # try:
    #   self.instrument_group
    #   return self.instrument_group.name + ' - ' + self.name
    # except InstrumentGroup.DoesNotExist:
    return self.name

  @staticmethod
  def parse_str_instrument_with_abbr(instrument_with_abbr: str) -> object:
    match = re.search('\((?P<abbreviation>\w+)\) (?P<name>[\w -]+)', instrument_with_abbr)
    instrument = None
    if match is not None:
      try:
        instrument = Instrument.objects.get(name=match.group('name'))
      except Instrument.DoesNotExist:
        instrument = Instrument(
          abbreviation = match.group('abbreviation'),
          name = match.group('name')
        )
    return instrument

  @staticmethod
  def parse_str_instruments(instruments: str) -> object:
    instruments_list = instruments.split(',')
    instruments_list = [Instrument.parse_str_instrument_with_abbr(instrument) for instrument in instruments_list]
    return [instrument for instrument in instruments_list if instrument is not None]

  @staticmethod
  def parse_str_accompaniments(instruments: str) -> object:
    instruments = re.sub('[0-9]+', '', instruments)
    instruments_list = []
    instruments_list = re.split(',|&|/|or |and ', instruments)
    instruments = []
    for i in instruments_list:
      if i not in ['Drums', 'Cymbals', 'Bass', 'Brass', 'Double Bass', 'String Bass']:
        i = re.sub('s$', '', i)
      i = re.sub('opt.|opt', '', i)
      i = i.strip().lstrip()
      try:
        instruments.append(Instrument.objects.get(name=i))
      except Instrument.DoesNotExist:
        pass
    return instruments

# ---

class ShelfLocation(models.Model):
  name = models.CharField(max_length=240)
  code = models.CharField(max_length=2)

  class Meta:
    ordering = ['code', 'name']
    verbose_name_plural = "Shelf Locations"

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def parse_str_shelf_location_with_code(shelf_location_with_code: str) -> object:
    match = re.search('\((?P<code>\w+)\) (?P<name>[\w \/\-()]+)', shelf_location_with_code)
    shelf_location = None
    if match is not None:
      try:
        shelf_location = ShelfLocation.objects.get(name=match.group('name'))
      except ShelfLocation.DoesNotExist:
        shelf_location = ShelfLocation(
          code = match.group('code'),
          name = match.group('name')
        )
    return shelf_location

  @staticmethod
  def parse_str_shelf_locations(shelf_locations: str) -> object:
    shelf_locations_list = shelf_locations.split(',')
    shelf_locations_list = [ShelfLocation.parse_str_shelf_location_with_code(shelf_location) for shelf_location in shelf_locations_list]
    return [shelf_location for shelf_location in shelf_locations_list if shelf_location is not None]

# ---

class Publisher(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

# ---

class Location(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def parse_str_locations(locations: str) -> object:
    locations_list = locations.split(',')
    locations_result = []
    for loc in locations_list:
      loc = loc.strip().lstrip()
      try:
        location = Location.objects.get(name=loc)
      except Location.DoesNotExist:
        location = Location(
          name = loc,
        )
      locations_result.append(location)
    return locations_result

# ---

def parse_full_name(full_name: str) -> object:
  first_name = None
  last_name = None
  match = re.search('(?P<last_name>[\w .\-\']+), (?P<first_name>[\w .\-\']+)', full_name)
  if match is not None:
    if not match.group('first_name') or not match.group('first_name').strip():
      first_name = "_"
    else:
      first_name = match.group('first_name').strip()
    if not match.group('last_name') or not match.group('last_name').strip():
      last_name = "_"
    else:
      last_name = match.group('last_name').strip()
  else:      
    first_name = "_"
    last_name = full_name.strip()

  return (first_name, last_name)

class Composer(models.Model):
  first_name = models.CharField(max_length=240)
  last_name = models.CharField(max_length=240)

  class Meta:
    ordering = ['last_name', 'first_name']

  def __str__(self) -> str:
    return self.last_name + ', ' + self.first_name

  @staticmethod
  def parse_str_composer_full_name(full_name: str) -> object:
    composer = None
    first_name, last_name = parse_full_name(full_name)
    try:
      composer = Composer.objects.get(first_name__iexact=first_name.lower(), last_name__iexact=last_name.lower())
    except Composer.DoesNotExist:
      composer = Composer(
        first_name = first_name,
        last_name = last_name
      )
    return composer

  @staticmethod
  def parse_str_composers(composers: str) -> object:
    if not composers or not composers.strip():
      return []
    composers_list = composers.split('/')
    composers_list = [Composer.parse_str_composer_full_name(composer) for composer in composers_list]
    return [composer for composer in composers_list if composer is not None]


# ---

class Arranger(models.Model):
  first_name = models.CharField(max_length=240)
  last_name = models.CharField(max_length=240)

  class Meta:
    ordering = ['last_name', 'first_name']

  def __str__(self) -> str:
    return self.last_name + ', ' + self.first_name

  @staticmethod
  def parse_str_arranger_full_name(full_name: str) -> object:
    arranger = None
    first_name, last_name = parse_full_name(full_name)

    try:
      arranger = Arranger.objects.get(first_name__iexact=first_name.lower(), last_name__iexact=last_name.lower())
    except Arranger.DoesNotExist:
      arranger = Arranger(
        first_name = first_name,
        last_name = last_name
      )
    return arranger

  @staticmethod
  def parse_str_arrangers(arrangers: str) -> object:
    arrangers_list = arrangers.split('/')
    arrangers_list = [Arranger.parse_str_arranger_full_name(arranger) for arranger in arrangers_list]
    return [arranger for arranger in arrangers_list if arranger is not None]

# ---

class EnsemblePart(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def parse_str_ensemble_parts(ensemble_parts: str) -> object:
    ensemble_parts_list = ensemble_parts.split(',')
    ensemble_parts_result = []
    for ep in ensemble_parts_list:
      ep = ep.strip().lstrip()
      try:
        ensemble_part = EnsemblePart.objects.get(name__iexact=ep.lower())
      except EnsemblePart.DoesNotExist:
        ensemble_part = EnsemblePart(
          name = ep,
        )
      ensemble_parts_result.append(ensemble_part)
    return ensemble_parts_result

# ---

class Sacred(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

# ---

class Grade(models.Model):
  name = models.IntegerField(default=1)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return str(self.name)

  @staticmethod
  def parse_str_grades(grades: str) -> object:
    grades = re.sub('\.5', '', grades)

    grades = re.sub('Preliminary', '0', grades, flags=re.IGNORECASE)
    grades = re.sub('Beginner', '0', grades, flags=re.IGNORECASE)
    grades = re.sub('Easy', '1', grades, flags=re.IGNORECASE)
    grades = re.sub('Low Intermediate', '2', grades, flags=re.IGNORECASE)
    grades = re.sub('Intermediate', '3', grades, flags=re.IGNORECASE)
    grades = re.sub('Medium', '3', grades, flags=re.IGNORECASE)
    grades = re.sub('Moderate', '3', grades, flags=re.IGNORECASE)
    grades = re.sub('Medium Difficult', '4', grades, flags=re.IGNORECASE)
    grades = re.sub('Advanced', '7', grades, flags=re.IGNORECASE)

    grades = re.sub('Prelim.|Prelim', '0', grades, flags=re.IGNORECASE)
    grades = re.sub('Interm.|Inter.|Interm|Inter', '3', grades, flags=re.IGNORECASE)
    grades = re.sub('Med.|Med', '3', grades, flags=re.IGNORECASE)
    grades = re.sub('Adv.|Adv', '7', grades, flags=re.IGNORECASE)

    grades_result = []
    if "-" in grades:
      grades_split = grades.split('-')
      start = int(grades_split[0].strip().lstrip())
      end = int(grades_split[1].strip().lstrip())
      i = start
      while i <= end:
        try:
          grade = Grade.objects.get(name=i)
        except Grade.DoesNotExist:
          grade = Grade(name=i)
        grades_result.append(grade)
        i += 1
    elif "," in grades:
      grades_split = grades.split(',')
      for grade in grades_split:
        grade = int(grade.strip().lstrip())
        try:
          grades_result.append(Grade.objects.get(name=grade))
        except Grade.DoesNotExist:
          grades_result.append(Grade(name=grade))
    elif "&" in grades:
      grades_split = grades.split('&')
      for grade in grades_split:
        grade = int(grade.strip().lstrip())
        try:
          grades_result.append(Grade.objects.get(name=grade))
        except Grade.DoesNotExist:
          grades_result.append(Grade(name=grade))
    return grades_result


# ---

class Genre(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def parse_str_genres(genres: str) -> object:
    genres_list = genres.split(',')
    genres_result = []
    for g in genres_list:
      g = g.strip().lstrip()
      try:
        genre = Genre.objects.get(name__iexact=g.lower())
      except Genre.DoesNotExist:
        genre = Genre(
          name = g,
        )
      genres_result.append(genre)
    return genres_result
# ---

class Status(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']
    verbose_name_plural = "Statuses"

  def __str__(self) -> str:
    return self.name

# ---

class Piece(models.Model):
  instruments = models.ManyToManyField(Instrument)
  instruments_secondary = models.ManyToManyField(Instrument, related_name='instruments_secondary', blank=True)
  shelf_locations = models.ManyToManyField(ShelfLocation)
  publisher = models.ForeignKey(Publisher, on_delete=PROTECT)
  locations = models.ManyToManyField(Location)

  # image = models.ImageField()

  catalogue_number = models.CharField(max_length=30)
  number_of_originals = models.IntegerField(default=1)
  number_of_copies = models.IntegerField(default=1)

  title = models.CharField(max_length=240)
  composers = models.ManyToManyField(Composer, blank=True)
  arrangers = models.ManyToManyField(Arranger, blank=True)
  isbn = models.CharField(max_length=250, null=True, blank=True)
  grades = models.ManyToManyField(Grade, blank=True)
 
  accompaniment = models.ManyToManyField(Instrument, related_name='instrument_accompaniment', blank=True)
  accompaniment_note = models.TextField(null=True, blank=True)
  missing_parts = models.TextField(null=True, blank=True)
  date_last_checked = models.DateField(auto_now_add=True)

  arrangement = models.CharField(max_length=50, null=True, blank=True)
  ensemble_parts = models.ManyToManyField(EnsemblePart, blank=True)
  soloists = models.ManyToManyField(Instrument, related_name='instrument_soloists', blank=True)
  sacred = models.BooleanField(default=False, null=True, blank=True)
  movements = models.IntegerField(default=1, null=True, blank=True)
  performance_time = models.DurationField(null=True, blank=True)
  genres = models.ManyToManyField(Genre, blank=True)
  medley = models.BooleanField(default=False, null=True, blank=True)

  related_file = models.TextField(null=True, blank=True)
  year_purchased = models.IntegerField(null=True, blank=True)
  year_last_performed = models.IntegerField(null=True, blank=True)

  status = models.ForeignKey(Status, on_delete=PROTECT, null=True, blank=True)

  song_list = models.TextField(null=True, blank=True)
  notes = models.TextField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  # class Meta:
  #   ordering = ['instrument', 'shelf_location', 'catalogue_number', 'title']

  def __str__(self) -> str:
    # return self.catalogue_number + " - " + self.title
    return self.title

  @staticmethod
  def last_cat_number(instrument: Instrument, shelf_location: ShelfLocation) -> str:
    try:
      return Piece.objects.filter(instruments=instrument, shelf_locations=shelf_location).order_by("-created_at")[0:1].get().catalogue_number
    except Piece.DoesNotExist:
      return None

  @staticmethod
  def suggested_cat_number(instrument: Instrument, shelf_location: ShelfLocation) -> str:
    catalogue_number = Piece.last_cat_number(instrument, shelf_location)
    number = 1
    if catalogue_number is not None:
      number = int(catalogue_number.split(".")[1])
      number += 1
    return instrument.abbreviation + '.' + shelf_location.code + '.' + f'{number:04}'
