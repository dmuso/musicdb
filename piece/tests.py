from django.test import TestCase
from .models import InstrumentGroup, Location, Piece, Category, Instrument, Publisher, Composer, Arranger, Grade, EnsemblePart

class PieceTestCase(TestCase):
  def setUp(self):
    Category.objects.create(name="AMEB", code="01")
    instrument_group = InstrumentGroup.objects.create(name="Woodwind")
    Instrument.objects.create(name="Flute", abbreviation="FL", instrument_group=instrument_group)
    Instrument.objects.create(name="Keyboard", abbreviation="KB", instrument_group=instrument_group)
    Instrument.objects.create(name="Guitar", abbreviation="GT", instrument_group=instrument_group)
    Instrument.objects.create(name="Oboe", abbreviation="OB", instrument_group=instrument_group)
    Instrument.objects.create(name="Clarinet", abbreviation="CL", instrument_group=instrument_group)
    Instrument.objects.create(name="Bassoon", abbreviation="BS", instrument_group=instrument_group)
    Instrument.objects.create(name="Double Bassoon", abbreviation="DB", instrument_group=instrument_group)
    Publisher.objects.create(name="Test Publisher")
    Location.objects.create(name="Test Location")

  def test_suggested_cat_number_returns_empty_with_no_instrument_selected(self):
    piece_first = Piece()
    self.assertEqual(piece_first.suggested_cat_number(), "")

  def test_suggested_cat_number_instrument_category_prefixes(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece(category=category, instrument=instrument, publisher=publisher, location=location)
    self.assertEqual(piece_first.suggested_cat_number(), instrument.abbreviation + category.code + ".0001")

  def test_suggested_cat_number_starts_at_one(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece(category=category, instrument=instrument, publisher=publisher, location=location)
    self.assertEqual(piece_first.suggested_cat_number(), instrument.abbreviation + category.code + ".0001")

  def test_suggested_cat_number_increments(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece.objects.create(category=category, instrument=instrument, catalogue_number=instrument.abbreviation + category.code + ".0001", publisher=publisher, location=location)
    piece_second = Piece(category=category, instrument=instrument, publisher=publisher, location=location)
    self.assertEqual(piece_second.suggested_cat_number(), instrument.abbreviation + category.code + ".0002")

  def test_last_cat_number_returns_empty_with_no_instrument_selected(self):
    piece_first = Piece()
    self.assertEqual(piece_first.last_cat_number(), "")

  def test_last_cat_number(self):
    category = Category.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece.objects.create(category=category, instrument=instrument, catalogue_number=instrument.abbreviation + category.code + ".0001", publisher=publisher, location=location)
    piece_second = Piece(category=category, instrument=instrument, publisher=publisher, location=location)
    self.assertEqual(piece_second.last_cat_number(), instrument.abbreviation + category.code + ".0001")

  def test_parse_str_instrument_with_abbr(self):
    instrument_with_abbr = "(GT) Guitar"
    instrument = Instrument.parse_str_instrument_with_abbr(instrument_with_abbr=instrument_with_abbr)
    self.assertEqual(instrument.abbreviation, "GT")
    self.assertEqual(instrument.name, "Guitar")

  def test_parse_str_instruments(self):
    instruments = "(GT) Guitar, (FL) Flute"
    instruments_list = Instrument.parse_str_instruments(instruments=instruments)
    self.assertEqual(len(instruments_list), 2)
    self.assertEqual(instruments_list[0].abbreviation, "GT")
    self.assertEqual(instruments_list[0].name, "Guitar")
    self.assertEqual(instruments_list[1].abbreviation, "FL")
    self.assertEqual(instruments_list[1].name, "Flute")

  def test_parse_str_category_with_code(self):
    category_with_code = "(10) AMEB"
    category = Category.parse_str_category_with_code(category_with_code=category_with_code)
    self.assertEqual(category.code, "01")
    self.assertEqual(category.name, "AMEB")

  def test_parse_str_categories(self):
    categories = "(16) Solo (Single), (20) Duet"
    categories_list = Category.parse_str_categories(categories=categories)
    self.assertEqual(len(categories_list), 2)
    self.assertEqual(categories_list[0].code, "16")
    self.assertEqual(categories_list[0].name, "Solo (Single)")
    self.assertEqual(categories_list[1].code, "20")
    self.assertEqual(categories_list[1].name, "Duet")

  def test_parse_str_composer_full_name(self):
    full_name = "Smith, John"
    composer = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer.first_name, "John")
    self.assertEqual(composer.last_name, "Smith")

  def test_parse_str_composers(self):
    composers = "Smith, John/Jones, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John")
    self.assertEqual(composers_list[0].last_name, "Smith")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "Jones")

  def test_parse_str_arranger_full_name(self):
    full_name = "Smith, John"
    arranger = Arranger.parse_str_arranger_full_name(full_name=full_name)
    self.assertEqual(arranger.first_name, "John")
    self.assertEqual(arranger.last_name, "Smith")

  def test_parse_str_arrangers(self):
    arrangers = "Smith, John/Jones, Mary"
    arrangers_list = Arranger.parse_str_arrangers(arrangers=arrangers)
    self.assertEqual(len(arrangers_list), 2)
    self.assertEqual(arrangers_list[0].first_name, "John")
    self.assertEqual(arrangers_list[0].last_name, "Smith")
    self.assertEqual(arrangers_list[1].first_name, "Mary")
    self.assertEqual(arrangers_list[1].last_name, "Jones")

  def test_parse_str_accompaniments(self):
    instruments = "Flute, Keyboard or Guitar"
    instruments_list = Instrument.parse_str_accompaniments(instruments=instruments)
    self.assertEqual(len(instruments_list), 3)
    self.assertEqual(instruments_list[0].name, "Flute")
    self.assertEqual(instruments_list[1].name, "Keyboard")
    self.assertEqual(instruments_list[2].name, "Guitar")

    instruments = "2 Oboes,2 Clarinets, 2 Horns, 2 Bassoons, opt. Double Bassoon or Doublebass"
    instruments_list = Instrument.parse_str_accompaniments(instruments=instruments)
    self.assertEqual(len(instruments_list), 4)
    self.assertEqual(instruments_list[0].name, "Oboe")
    self.assertEqual(instruments_list[1].name, "Clarinet")
    self.assertEqual(instruments_list[2].name, "Bassoon")
    self.assertEqual(instruments_list[3].name, "Double Bassoon")

  def test_parse_str_grades(self):
    grades = "1-3"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 3)
    self.assertEqual(grades_list[0].name, 1)
    self.assertEqual(grades_list[1].name, 2)
    self.assertEqual(grades_list[2].name, 3)

  def test_parse_str_grades(self):
    grades = "1 - 3"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 3)
    self.assertEqual(grades_list[0].name, 1)
    self.assertEqual(grades_list[1].name, 2)
    self.assertEqual(grades_list[2].name, 3)

  def test_parse_str_grades(self):
    grades = "4 - 4.5"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 1)
    self.assertEqual(grades_list[0].name, 4)

  def test_parse_str_grades(self):
    grades = "4.5 - 5"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 2)
    self.assertEqual(grades_list[0].name, 4)
    self.assertEqual(grades_list[1].name, 5)

  def test_parse_str_grades(self):
    grades = "1,3"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 2)
    self.assertEqual(grades_list[0].name, 1)
    self.assertEqual(grades_list[1].name, 3)

  def test_parse_str_grades(self):
    grades = "3.5"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 1)
    self.assertEqual(grades_list[0].name, 3)

  def test_parse_str_grades(self):
    grades = "1 & 3"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 2)
    self.assertEqual(grades_list[0].name, 1)
    self.assertEqual(grades_list[1].name, 3)

  def test_parse_str_grades(self):
    grades = "Easy-Medium"
    grades_list = Grade.parse_str_grades(grades=grades)
    self.assertEqual(len(grades_list), 3)
    self.assertEqual(grades_list[0].name, 1)
    self.assertEqual(grades_list[1].name, 2)
    self.assertEqual(grades_list[2].name, 3)

  def test_parse_str_ensemble_parts(self):
    ensemble_parts = "4 Part, SATB, Carols for Choirs"
    ensemble_parts_list = EnsemblePart.parse_str_ensemble_parts(ensemble_parts=ensemble_parts)
    self.assertEqual(len(ensemble_parts_list), 3)
    self.assertEqual(ensemble_parts_list[0].name, '4 Part')
    self.assertEqual(ensemble_parts_list[1].name, 'SATB')
    self.assertEqual(ensemble_parts_list[2].name, 'Carols for Choirs')

