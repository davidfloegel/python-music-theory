"""Interval Test"""
import unittest
from nose.tools import assert_raises

from .note import Note
from .interval import Interval


class IntervalTest(unittest.TestCase):
    """Interval Test"""

    @classmethod
    def test_invalid_quality(cls):
        """Test if exceptions is thrown if invalid quality."""
        assert_raises(ValueError, Interval, "X", 4)
        assert_raises(ValueError, Interval, "M", 4)

    @classmethod
    def test_invalid_quantity(cls):
        """Test if exceptions is thrown if invalid quantity."""
        assert_raises(ValueError, Interval, "M", 0)
        assert_raises(ValueError, Interval, "M", 9)

    @classmethod
    def test_invalid_interval(cls):
        """Test if exceptions is thrown if interval is invalid"""
        assert_raises(ValueError, Interval.from_string, "Q3")
        assert_raises(ValueError, Interval.from_string, "R5")
        assert_raises(ValueError, Interval.from_string, "N9")

    @classmethod
    def test_new_interval(cls):
        """Test initialising a new interval with quality and quantity"""
        interval = Interval("P", 4)
        assert interval.name == "P4"

        interval = Interval("M", 3)
        assert interval.name == "M3"

        interval = Interval("m", 2)
        assert interval.name == "m2"

        interval = Interval("A", 5)
        assert interval.name == "A5"

        interval = Interval("d", 4)
        assert interval.name == "d4"

    @classmethod
    def test_new_interval_from_string(cls):
        """Test initialising new interval from string"""
        interval = Interval.from_string("P4")
        assert interval.name == "P4"

        interval = Interval.from_string("M3")
        assert interval.name == "M3"

    @classmethod
    def test_from_quantity_semitones(cls):
        """Test initialising new interval from quantity and semitones."""
        assert Interval.from_quantity_and_semitones(3, 4).name == "M3"
        assert Interval.from_quantity_and_semitones(6, 9).name == "M6"
        assert Interval.from_quantity_and_semitones(6, 8).name == "m6"

    @classmethod
    def test_invalid_qty_semitones(cls):
        """Test if exception is thrown if quantity and semitones are invalid"""
        assert_raises(LookupError, Interval.from_quantity_and_semitones, 14, 2)

    @classmethod
    def test_invert_interval(cls):
        """Test inverting an interval"""
        interval = Interval.from_string("M2")
        assert interval.invert().name == 'm7'

        interval = Interval.from_string("m3")
        assert interval.invert().name == 'M6'

        interval = Interval.from_string("P4")
        assert interval.invert().name == 'P5'

        interval = Interval.from_string("A5")
        assert interval.invert().name == 'd4'

        interval = Interval.from_string("d6")
        assert interval.invert().name == 'A3'

    @classmethod
    def _note_add(cls, root, interval):
        """Add a note to another note"""
        return (Note(root) + Interval.from_string(interval)).name

    @classmethod
    def _note_sub(cls, root, interval):
        """Subtract a note from another note"""
        return (Note(root) - Interval.from_string(interval)).name

    @classmethod
    def _note_roundtrip(cls, root, interval):
        """Round Trip on Notes"""
        return cls._note_sub(cls._note_add(root, interval), interval)

    @classmethod
    def test_interval_addition(cls):
        """Test adding INTERVALS to a root note"""
        assert cls._note_add('C', 'P1') == 'C'
        assert cls._note_add('Eb', 'd4') == 'Abb'
        assert cls._note_add('Eb', 'm3') == 'Gb'
        assert cls._note_add('Eb', 'A2') == 'F#'
        assert cls._note_add('Eb', 'M2') == 'F'
        assert cls._note_add('Eb', 'd3') == 'Gbb'
        assert cls._note_add('D#', 'M3') == 'F##'
        assert cls._note_add('D#', 'd4') == 'G'

        # test octave adjustment
        target = Note('B') + Interval.from_string('M2')
        assert target.name == 'C#'
        assert target.octave == 5

    @classmethod
    def test_interval_subtraction(cls):
        """Test subtracting INTERVALS from a root note"""
        assert cls._note_sub('C', 'P1') == 'C'
        assert cls._note_sub('G', 'M3') == 'Eb'
        assert cls._note_sub('Abb', 'd4') == 'Eb'
        assert cls._note_sub('Gb', 'm3') == 'Eb'
        assert cls._note_sub('F#', 'A2') == 'Eb'
        assert cls._note_sub('F', 'M2') == 'Eb'
        assert cls._note_sub('Gbb', 'd3') == 'Eb'
        assert cls._note_sub('F##', 'M3') == 'D#'
        assert cls._note_sub('G', 'd4') == 'D#'

        # test octave adjustment
        target = Note('D') - Interval.from_string('P5')
        assert target.name == 'G'
        assert target.octave == 3

    @classmethod
    def test_interval_roundtrip(cls):
        """Test a whole round trip on INTERVALS"""
        assert cls._note_roundtrip('C', 'P1') == 'C'
        assert cls._note_roundtrip('Eb', 'M3') == 'Eb'
        assert cls._note_roundtrip('Eb', 'd4') == 'Eb'
        assert cls._note_roundtrip('Eb', 'm3') == 'Eb'
        assert cls._note_roundtrip('Eb', 'A2') == 'Eb'
        assert cls._note_roundtrip('Eb', 'M2') == 'Eb'
        assert cls._note_roundtrip('Eb', 'M6') == 'Eb'
        assert cls._note_roundtrip('D#', 'M3') == 'D#'
        assert cls._note_roundtrip('D#', 'd4') == 'D#'

    @classmethod
    def _note_minus_note(cls, root, target):
        """Perform Note - Note"""
        return ((Note(root)).minus_note(Note(target))).name

    @classmethod
    def test_note_minus_note_asc(cls):
        """Note - Note ascending"""
        # within one octave
        assert cls._note_minus_note("C", "C") == "P1"
        assert cls._note_minus_note("C", "D") == "M2"
        assert cls._note_minus_note("C", "E") == "M3"
        assert cls._note_minus_note("C", "F") == "P4"
        assert cls._note_minus_note("C", "G") == "P5"
        assert cls._note_minus_note("C", "A") == "M6"
        assert cls._note_minus_note("C", "B") == "M7"
        assert cls._note_minus_note("C", "C5") == "P8"

        # with accidentals
        assert cls._note_minus_note("C", "Db") == "m2"
        assert cls._note_minus_note("C", "Eb") == "m3"
        assert cls._note_minus_note("C", "Fb") == "d4"
        assert cls._note_minus_note("C", "Gb") == "d5"
        assert cls._note_minus_note("C", "Ab") == "m6"
        assert cls._note_minus_note("C", "Bb") == "m7"
        assert cls._note_minus_note("C", "D#") == "A2"
        assert cls._note_minus_note("C", "E#") == "A3"
        assert cls._note_minus_note("C", "F#") == "A4"
        assert cls._note_minus_note("C", "G#") == "A5"
        assert cls._note_minus_note("C", "A#") == "A6"
        assert cls._note_minus_note("C", "B#") == "A7"
        assert cls._note_minus_note("Eb", "G") == "M3"

        # across two octaves
        assert cls._note_minus_note("Bb", "C5") == "M2"
        assert cls._note_minus_note("Bb", "Db5") == "m3"
        assert cls._note_minus_note("Bb", "D5") == "M3"
        assert cls._note_minus_note("Bb", "Eb5") == "P4"
        assert cls._note_minus_note("Bb", "E5") == "A4"
        assert cls._note_minus_note("Bb", "F5") == "P5"
        assert cls._note_minus_note("Bb", "Gb5") == "m6"
        assert cls._note_minus_note("Bb", "G5") == "M6"
        assert cls._note_minus_note("Bb", "Ab5") == "m7"
        assert cls._note_minus_note("Bb", "A5") == "M7"
        assert cls._note_minus_note("Bb", "Bb5") == "P8"

    @classmethod
    def test_note_minus_note_desc(cls):
        """Note - Note descending"""
        # within one octave
        assert cls._note_minus_note("B", "B") == "P1"
        assert cls._note_minus_note("B", "A") == "M2"
        assert cls._note_minus_note("B", "G") == "M3"
        assert cls._note_minus_note("B", "F") == "A4"
        assert cls._note_minus_note("B", "F#") == "P4"
        assert cls._note_minus_note("B", "E") == "P5"
        assert cls._note_minus_note("B", "D") == "M6"
        assert cls._note_minus_note("B", "C") == "M7"
        assert cls._note_minus_note("B", "B3") == "P8"

        # across two octaves
        assert cls._note_minus_note("C", "B3") == "m2"
        assert cls._note_minus_note("C", "A3") == "m3"
        assert cls._note_minus_note("C", "G3") == "P4"
        assert cls._note_minus_note("C", "F3") == "P5"
        assert cls._note_minus_note("C", "E3") == "m6"
        assert cls._note_minus_note("C", "D3") == "m7"
        assert cls._note_minus_note("C", "C3") == "P8"

        # with accidentals
        assert cls._note_minus_note("C", "Bb3") == "M2"
        assert cls._note_minus_note("C", "Ab3") == "M3"
        assert cls._note_minus_note("C", "Gb3") == "A4"
        assert cls._note_minus_note("C", "Fb3") == "A5"
        assert cls._note_minus_note("C", "Eb3") == "M6"
        assert cls._note_minus_note("C", "Db3") == "M7"
