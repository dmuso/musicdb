from django.test import TestCase
from .models import InstrumentGroup, Location, Piece, ShelfLocation, Instrument, Publisher, Composer, Arranger, Grade, EnsemblePart, Genre

class PieceTestCase(TestCase):
  def setUp(self):
    ShelfLocation.objects.create(name="AMEB", code="01")
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

  def test_suggested_cat_number_starts_at_one(self):
    shelf_location = ShelfLocation.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")

    self.assertEqual(Piece.suggested_cat_number(instrument, shelf_location), instrument.abbreviation + shelf_location.code + ".0001")

  def test_suggested_cat_number_increments(self):
    shelf_location = ShelfLocation.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece.objects.create(
      title="Test Piece",
      catalogue_number=instrument.abbreviation + shelf_location.code + ".0001",
      publisher=publisher
    )
    piece_first.save()
    piece_first.instruments.add(instrument)
    piece_first.shelf_locations.add(shelf_location)
    piece_first.locations.add(location)
    self.assertEqual(Piece.suggested_cat_number(instrument, shelf_location), instrument.abbreviation + shelf_location.code + ".0002")

  def test_last_cat_number(self):
    shelf_location = ShelfLocation.objects.get(name="AMEB")
    instrument = Instrument.objects.get(name="Flute")
    publisher = Publisher.objects.get(name="Test Publisher")
    location = Location.objects.get(name="Test Location")

    piece_first = Piece.objects.create(
      title="Test Piece",
      catalogue_number=instrument.abbreviation + shelf_location.code + ".0001",
      publisher=publisher
    )
    piece_first.save()
    piece_first.instruments.add(instrument)
    piece_first.shelf_locations.add(shelf_location)
    piece_first.locations.add(location)

    self.assertEqual(Piece.last_cat_number(instrument, shelf_location), instrument.abbreviation + shelf_location.code + ".0001")

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

  def test_parse_str_instruments_space(self):
    instruments = "(MM) Multi Percussion, (MP) Multi-Percussion"
    instruments_list = Instrument.parse_str_instruments(instruments=instruments)
    self.assertEqual(len(instruments_list), 2)
    self.assertEqual(instruments_list[0].abbreviation, "MM")
    self.assertEqual(instruments_list[0].name, "Multi Percussion")
    self.assertEqual(instruments_list[1].abbreviation, "MP")
    self.assertEqual(instruments_list[1].name, "Multi-Percussion")

  def test_parse_str_shelf_location_with_code(self):
    shelf_location_with_code = "(10) AMEB"
    shelf_location = ShelfLocation.parse_str_shelf_location_with_code(shelf_location_with_code=shelf_location_with_code)
    self.assertEqual(shelf_location.code, "01")
    self.assertEqual(shelf_location.name, "AMEB")

  def test_parse_str_shelf_location_with_code_and_slash(self):
    shelf_location_with_code = "(05) Jazz/Blues"
    shelf_location = ShelfLocation.parse_str_shelf_location_with_code(shelf_location_with_code=shelf_location_with_code)
    self.assertEqual(shelf_location.code, "05")
    self.assertEqual(shelf_location.name, "Jazz/Blues")

  def test_parse_str_shelf_location_with_code_and_dash(self):
    shelf_location_with_code = "(13) CD-ROM Library"
    shelf_location = ShelfLocation.parse_str_shelf_location_with_code(shelf_location_with_code=shelf_location_with_code)
    self.assertEqual(shelf_location.code, "13")
    self.assertEqual(shelf_location.name, "CD-ROM Library")

  def test_parse_str_shelf_locations(self):
    shelf_locations = "(16) Solo (Single), (20) Duet"
    shelf_locations_list = ShelfLocation.parse_str_shelf_locations(shelf_locations=shelf_locations)
    self.assertEqual(len(shelf_locations_list), 2)
    self.assertEqual(shelf_locations_list[0].code, "16")
    self.assertEqual(shelf_locations_list[0].name, "Solo (Single)")
    self.assertEqual(shelf_locations_list[1].code, "20")
    self.assertEqual(shelf_locations_list[1].name, "Duet")

  def test_parse_str_locations(self):
    locations = "SS - Music 2, SS - Music 5"
    locations_list = Location.parse_str_locations(locations=locations)
    self.assertEqual(len(locations_list), 2)
    self.assertEqual(locations_list[0].name, "SS - Music 2")
    self.assertEqual(locations_list[1].name, "SS - Music 5")

  def test_parse_str_composer_full_name(self):
    full_name = "Smith, John"
    composer = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer.first_name, "John")
    self.assertEqual(composer.last_name, "Smith")

  def test_parse_str_composer_full_name_reuses(self):
    full_name = "Smith, John"
    composer1 = Composer.parse_str_composer_full_name(full_name=full_name)
    composer2 = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer1.pk, composer2.pk)

  def test_parse_str_composer_band(self):
    full_name = "The Beatles"
    composer = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer.first_name, "_")
    self.assertEqual(composer.last_name, "The Beatles")

  def test_parse_str_composer_band_reuses(self):
    full_name = "The Beatles"
    composer1 = Composer.parse_str_composer_full_name(full_name=full_name)
    composer1.save()
    composer2 = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer1.pk, composer2.pk)

  def test_parse_str_composer_band_reuses_case(self):
    full_name1 = "The Beatles"
    full_name2 = "the beatles"
    composer1 = Composer.parse_str_composer_full_name(full_name=full_name1)
    composer1.save()
    composer2 = Composer.parse_str_composer_full_name(full_name=full_name2)
    self.assertEqual(composer1.pk, composer2.pk)

  def test_parse_str_composer_band_one_word(self):
    full_name = "Beatles"
    composer = Composer.parse_str_composer_full_name(full_name=full_name)
    self.assertEqual(composer.first_name, "_")
    self.assertEqual(composer.last_name, "Beatles")

  def test_parse_str_composers_empty(self):
    composers = ""
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 0)

  def test_parse_str_composers_basic(self):
    composers = "Smith, John/Jones, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John")
    self.assertEqual(composers_list[0].last_name, "Smith")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "Jones")

  def test_parse_str_composers_basic_reuses(self):
    composers = "Smith, John/Jones, Mary"
    composers_list1 = Composer.parse_str_composers(composers=composers)
    composers_list2 = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list1), 2)
    self.assertEqual(composers_list1[0].pk, composers_list1[1].pk)
    self.assertEqual(composers_list2[0].pk, composers_list2[1].pk)

  def test_parse_str_composers_basic_reuses_case(self):
    composers1 = "Smith, John/Jones, Mary"
    composers2 = "smith , john "
    composers_list1 = Composer.parse_str_composers(composers=composers1)
    composers_list2 = Composer.parse_str_composers(composers=composers2)
    self.assertEqual(composers_list1[0].pk, composers_list2[0].pk)

  def test_parse_str_composers_apos(self):
    composers = "Smith, John/O'Reilly, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John")
    self.assertEqual(composers_list[0].last_name, "Smith")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "O'Reilly")

  def test_parse_str_composers_hyphen(self):
    composers = "Clayton-Thomas, John/O'Reilly, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John")
    self.assertEqual(composers_list[0].last_name, "Clayton-Thomas")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "O'Reilly")

  def test_parse_str_composers_super_hyphen(self):
    composers = "Clayton-Thomas, Daniel-Thomas/O'Reilly, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "Daniel-Thomas")
    self.assertEqual(composers_list[0].last_name, "Clayton-Thomas")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "O'Reilly")

  def test_parse_str_composers_space(self):
    composers = "De Haan, John Boy/O'Reilly, Mary"
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John Boy")
    self.assertEqual(composers_list[0].last_name, "De Haan")
    self.assertEqual(composers_list[1].first_name, "Mary")
    self.assertEqual(composers_list[1].last_name, "O'Reilly")

  def test_parse_str_composers_initials(self):
    composers = "Smith, John F/Jones, Mary J. S."
    composers_list = Composer.parse_str_composers(composers=composers)
    self.assertEqual(len(composers_list), 2)
    self.assertEqual(composers_list[0].first_name, "John F")
    self.assertEqual(composers_list[0].last_name, "Smith")
    self.assertEqual(composers_list[1].first_name, "Mary J. S.")
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

  def test_parse_str_genres(self):
    genres = "Ballet, Classical, Romantic Period"
    genres_list = Genre.parse_str_genres(genres=genres)
    self.assertEqual(len(genres_list), 3)
    self.assertEqual(genres_list[0].name, 'Ballet')
    self.assertEqual(genres_list[1].name, 'Classical')
    self.assertEqual(genres_list[2].name, 'Romantic Period')

