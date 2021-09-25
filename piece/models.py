from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models import UniqueConstraint

# ---

class InstrumentGroup(models.Model):
  name = models.CharField(max_length=240)
  abbreviation = models.CharField(max_length=2)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name + ' (' + self.abbreviation + ')'

  # UniqueConstraint(fields=['name'], name='unique_instrument_name')
  # UniqueConstraint(fields=['abbreviation'], name='unique_instrument_abbreviation')

# ---

class Instrument(models.Model):
  instrument_group = models.ForeignKey(InstrumentGroup, on_delete=PROTECT)
  name = models.CharField(max_length=240)
  abbreviation = models.CharField(max_length=2)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name + ' (' + self.abbreviation + ')'

  # UniqueConstraint(fields=['name'], name='unique_instrument_name')
  # UniqueConstraint(fields=['abbreviation'], name='unique_instrument_abbreviation')

# ---

class Category(models.Model):
  name = models.CharField(max_length=240)
  code = models.CharField(max_length=2)

  class Meta:
    ordering = ['code', 'name']

  def __str__(self) -> str:
    return '(' + self.code + ') ' + self.name

  # UniqueConstraint(fields=['name'], name='unique_category_name')
  # UniqueConstraint(fields=['code'], name='unique_category_code')

# ---

class Publisher(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  # UniqueConstraint(fields=['name'], name='unique_category_name')
  # UniqueConstraint(fields=['code'], name='unique_category_code')

# ---

class Location(models.Model):
  name = models.CharField(max_length=240)

  class Meta:
    ordering = ['name']

  def __str__(self) -> str:
    return self.name

  # UniqueConstraint(fields=['name'], name='unique_category_name')
  # UniqueConstraint(fields=['code'], name='unique_category_code')

# ---

class Composer(models.Model):
  first_name = models.CharField(max_length=240)
  last_name = models.CharField(max_length=240)

  class Meta:
    ordering = ['last_name', 'first_name']

  def __str__(self) -> str:
    return self.last_name + ', ' + self.first_name

  # UniqueConstraint(fields=['name'], name='unique_category_name')
  # UniqueConstraint(fields=['code'], name='unique_category_code')

# ---

class Piece(models.Model):
  instrument = models.ForeignKey(Instrument, on_delete=PROTECT)
  category = models.ForeignKey(Category, on_delete=PROTECT)
  publisher = models.ForeignKey(Publisher, on_delete=PROTECT)
  location = models.ForeignKey(Location, on_delete=PROTECT)

  grade = models.CharField(max_length=30)
  
  catalogue_number = models.CharField(max_length=30)
  number_of_copies = models.IntegerField(default=1)

  title = models.CharField(max_length=240)
  accompaniment = models.ManyToManyField(Instrument, related_name='instrument_accompaniment')
  composers = models.ManyToManyField(Composer)
  isbn = models.CharField(max_length=50)

  missing_parts = models.CharField(max_length=240)
  date_last_checked = models.DateTimeField

  # notes =

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['instrument', 'category', 'catalogue_number', 'title']

  def __str__(self) -> str:
    return self.title

  def last_cat_number(self) -> str:
    if hasattr(self, 'instrument') and hasattr(self, 'category'):
      try:
        return Piece.objects.filter(instrument=self.instrument, category=self.category).order_by("-created_at")[0:1].get().catalogue_number
      except self.DoesNotExist:
        return ""
    else:
      return ""

  def suggested_cat_number(self) -> str:
    if hasattr(self, 'instrument') and hasattr(self, 'category'):
      catalogue_number = self.last_cat_number()
      if catalogue_number != "":
        number = int(catalogue_number.split(".")[1])
        number += 1
      else:
        number = 1
      return self.instrument.abbreviation + self.category.code + '.' + f'{number:04}'
    else:
      return ""
