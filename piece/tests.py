from django.test import TestCase
from .models import Piece, Category, Instrument

class PieceTestCase(TestCase):
  def setUp(self):
    Category.objects.create(name="AMEB", code="01")
    Instrument.objects.create(name="Flute", abbreviation="FL")

  def test_suggested_cat_number_returns_empty_with_no_instrument_selected(self):
    piece_first = Piece()
    self.assertEqual(piece_first.suggested_cat_number(), "")

  def test_suggested_cat_number_instrument_category_prefixes(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    piece_first = Piece(category=category, instrument=instrument)
    self.assertEqual(piece_first.suggested_cat_number(), instrument.abbreviation + category.code + ".0001")

  def test_suggested_cat_number_starts_at_one(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    piece_first = Piece(category=category, instrument=instrument)
    self.assertEqual(piece_first.suggested_cat_number(), instrument.abbreviation + category.code + ".0001")

  def test_suggested_cat_number_increments(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    piece_first = Piece.objects.create(category=category, instrument=instrument, catalogue_number=instrument.abbreviation + category.code + ".0001")
    piece_second = Piece(category=category, instrument=instrument)
    self.assertEqual(piece_second.suggested_cat_number(), instrument.abbreviation + category.code + ".0002")

  def test_last_cat_number_returns_empty_with_no_instrument_selected(self):
    piece_first = Piece()
    self.assertEqual(piece_first.last_cat_number(), "")

  def test_last_cat_number(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    piece_first = Piece.objects.create(category=category, instrument=instrument, catalogue_number=instrument.abbreviation + category.code + ".0001")
    piece_second = Piece(category=category, instrument=instrument)
    self.assertEqual(piece_second.last_cat_number(), instrument.abbreviation + category.code + ".0001")

