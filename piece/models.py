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
  instrument = models.ForeignKey(Instrument, on_delete=PROTECT)
  category = models.ForeignKey(Category, on_delete=PROTECT)
  # grade = 
  
  catalogue_number = models.CharField(max_length=30)
  number_of_copies = models.IntegerField(default=1)
  # location = 

  title = models.CharField(max_length=240)
  # accompaniment =
  # composer = 
  # publisher = 
  # isbn =

  # missing_parts =
  # date_last_checked =

  # notes =

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

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
