from django.db import models
from django.db.models.deletion import PROTECT
from instrument.models import Instrument

class Piece(models.Model):
  # catalogue_number = 
  number_of_copies = models.IntegerField(default=1)
  # location = 

  instrument = models.ForeignKey(Instrument, on_delete=PROTECT)
  # category = 
  # grade = 
  
  title = models.CharField(max_length=240)
  # accompaniment =
  # composer = 
  # publisher = 
  # isbn =

  # missing_parts =
  # date_last_checked =

  # notes =