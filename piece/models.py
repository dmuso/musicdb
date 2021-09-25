from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models import UniqueConstraint
# from piece.models.Piece.instrument import RelatedObjectDoesNotExist

# ---

class Instrument(models.Model):
  name = models.CharField(max_length=240)
  abbreviation = models.CharField(max_length=2)

  def __str__(self) -> str:
    return self.name + ' (' + self.abbreviation + ')'

  # UniqueConstraint(fields=['name'], name='unique_instrument_name')
  # UniqueConstraint(fields=['abbreviation'], name='unique_instrument_abbreviation')

# ---

class Category(models.Model):
  name = models.CharField(max_length=240)
  code = models.CharField(max_length=2)

  def __str__(self) -> str:
    return '(' + self.code + ') ' + self.name

  # UniqueConstraint(fields=['name'], name='unique_category_name')
  # UniqueConstraint(fields=['code'], name='unique_category_code')

# ---

class Piece(models.Model):
  # catalogue_number = 
  number_of_copies = models.IntegerField(default=1)
  # location = 

  instrument = models.ForeignKey(Instrument, on_delete=PROTECT)
  category = models.ForeignKey(Category, on_delete=PROTECT)
  # grade = 
  
  title = models.CharField(max_length=240)
  # accompaniment =
  # composer = 
  # publisher = 
  # isbn =

  # missing_parts =
  # date_last_checked =

  # notes =

  def __str__(self) -> str:
    return self.title

  def suggested_cat_code(self) -> str:
    if hasattr(self, 'instrument') and hasattr(self, 'category'):
      return self.instrument.abbreviation + self.category.code
    else:
      return ""
