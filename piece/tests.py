from django.test import TestCase
from .models import Piece, Category, Instrument

class PieceTestCase(TestCase):
  def setUp(self):
    Category.objects.create(name="AMEB", code="01")
    Instrument.objects.create(name="Flute", abbreviation="FL")

  def test_suggested_cat_code_returns_empty_with_no_instrument_selected(self):
    category = Category.objects.get(name="AMEB")
    piece_first = Piece()
    self.assertEqual(piece_first.suggested_cat_code(), "")

  def test_suggested_cat_code_instrument_category_prefixes(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    piece_first = Piece(category=category, instrument=instrument)
    self.assertEqual(piece_first.suggested_cat_code(), instrument.abbreviation + category.code)
