from django.db import models
from django.db.models import UniqueConstraint

class Instrument(models.Model):
  name = models.CharField(max_length=240)
  abbreviation = models.CharField(max_length=2)

UniqueConstraint(fields=['name'], name='unique_instrument_name')
UniqueConstraint(fields=['abbreviation'], name='unique_instrument_abbreviation')
