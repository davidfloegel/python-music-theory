"""Accidentals Test"""
import unittest
from nose.tools import assert_raises

from .accidentals import Accidentals


class AccidentalsTest(unittest.TestCase):
    """Accidentals Test"""

    @classmethod
    def test_invalid_accidentals(cls):
        """Test if exceptions is thrown if accidentals are invalid."""
        assert_raises(ValueError, Accidentals, 'd')
        assert_raises(ValueError, Accidentals, 'i')
        assert_raises(ValueError, Accidentals, '##b')
        assert_raises(ValueError, Accidentals, 'xxb')

    @classmethod
    def test_initialise_new_accidentals(cls):
        """
        Test if accidental has been initialised and all relevant members
        are present
        """
        accidental = Accidentals('#x')
        assert accidental.accidentals == '#x'
        assert accidental.sanitised == ['#', '#', '#']
        assert accidental.value == +3

    @classmethod
    def test_calculate_interval_value(cls):
        """Calculate adjustment value (used for intervals)"""
        accidental = Accidentals()
        assert accidental.value == 0

        # FLATs
        accidental = Accidentals('b')
        assert accidental.value == -1
        accidental = Accidentals('bb')
        assert accidental.value == -2
        accidental = Accidentals('bbb')
        assert accidental.value == -3

        # SHARPs
        accidental = Accidentals('#')
        assert accidental.value == +1
        accidental = Accidentals('x')
        assert accidental.value == +2
        accidental = Accidentals('#x')
        assert accidental.value == +3
