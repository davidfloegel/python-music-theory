"""Note Test"""
import unittest
from nose.tools import assert_raises

from .note import Note


class NoteTest(unittest.TestCase):
    """Note Test"""

    @classmethod
    def test_invalid_syntax(cls):
        """Test if exceptions is thrown if note syntax is invalid."""
        # invalid letter
        assert_raises(ValueError, Note, "W")
        assert_raises(ValueError, Note, "U")

        # invlid accidental
        assert_raises(ValueError, Note, "E%")
        assert_raises(ValueError, Note, "E/")

        assert_raises(ValueError, Note, "C12")
        assert_raises(ValueError, Note, "F#12")

    @classmethod
    def test_note_from_index(cls):
        """Test returning a Note instance from semitones"""
        assert Note.from_index(1).name == 'C'
        assert Note.from_index(2).name == 'D'
        assert Note.from_index(3).name == 'E'
        assert Note.from_index(4).name == 'F'
        assert Note.from_index(5).name == 'G'
        assert Note.from_index(6).name == 'A'
        assert Note.from_index(7).name == 'B'

    @classmethod
    def test_extract_note_letter(cls):
        """Test extraction of the NOTES letter without accidetals."""
        note = Note('C')
        assert note.letter == 'C'

        note = Note('Eb')
        assert note.letter == 'E'

    @classmethod
    def test_extract_note_accidentals(cls):
        """Test extraction of the NOTES accidental string."""
        note = Note('F')
        assert note.accidentals.accidentals == ''

        note = Note('Ab')
        assert note.accidentals.accidentals == 'b'

        note = Note('C##')
        assert note.accidentals.accidentals == '##'

    @classmethod
    def test_extract_note_octave(cls):
        """Test extraction of note octave"""
        note = Note("G")
        assert note.octave == 4

        note = Note("C5")
        assert note.octave == 5

        note = Note("F#2")
        assert note.octave == 2

        note = Note("Eb3")
        assert note.octave == 3

    @classmethod
    def test_calculate_midi_value(cls):
        """Test the calculation of the NOTES midi value."""
        note = Note('C')
        assert note.midi_value == 60

        note = Note('Eb')
        assert note.midi_value == 63

        note = Note('Bb5')
        assert note.midi_value == 82

        note = Note('A#3')
        assert note.midi_value == 58

    @classmethod
    def test_calc_easy_notation(cls):
        """Test the calculation of the enharmonic equivalent"""
        # Notes that don't get an enharmonic equivalent
        assert Note('C').easy_notation is None
        assert Note('Bb').easy_notation is None
        assert Note('F#').easy_notation is None

        # octave changing alternatives
        note = Note('Cb')
        assert note.easy_notation.name == Note('B').name
        assert note.easy_notation.octave == 3

        assert Note('Cbb').easy_notation.name == Note('Bb').name
        assert Note('Cbbb').easy_notation.name == Note('A').name

        note = Note('B#')
        assert note.easy_notation.name == Note('C').name
        assert note.easy_notation.octave == 5

        assert Note('Bx').easy_notation.name == Note('C#').name
        assert Note('B#x').easy_notation.name == Note('D').name

        # easy examples
        assert Note('Fb').easy_notation.name == Note('E').name
        assert Note('Fbb').easy_notation.name == Note('Eb').name
        assert Note('Fbbb').easy_notation.name == Note('D').name
        assert Note('E#').easy_notation.name == Note('F').name
        assert Note('Ex').easy_notation.name == Note('F#').name
        assert Note('E##').easy_notation.name == Note('F#').name
        assert Note('E#x').easy_notation.name == Note('G').name
        assert Note('E###').easy_notation.name == Note('G').name

        # more easy ones
        assert Note('Abb').easy_notation.name == Note('G').name
        assert Note('Abbb').easy_notation.name == Note('Gb').name
        assert Note('G##').easy_notation.name == Note('A').name
        assert Note('Gx').easy_notation.name == Note('A').name
        assert Note('G###').easy_notation.name == Note('A#').name
        assert Note('G#x').easy_notation.name == Note('A#').name

    @classmethod
    def test_enharmonic_comparison(cls):
        """Test if two NOTES are enharmonically the same"""
        assert Note('C#') == Note('Db')
        assert Note('E#') == Note('F')
        assert Note('Abb') == Note('G')

    @classmethod
    def test_comparison(cls):
        """Test if two NOTES are enharmonically the same"""
        assert Note('C#').is_same(Note('C#'))
        assert Note('E#').is_same(Note('E#'))
        assert Note('Abb').is_same(Note('Abb'))

    @classmethod
    def test_note_distance_calculation(cls):
        """Calculate distance between 2 NOTES"""
        # plain NOTES
        assert Note('C').calc_distance_to(Note('C')) == (1, 0)
        assert Note('C').calc_distance_to(Note('D')) == (2, 2)
        assert Note('C').calc_distance_to(Note('E')) == (3, 4)
        assert Note('C').calc_distance_to(Note('F')) == (4, 5)
        assert Note('C').calc_distance_to(Note('G')) == (5, 7)
        assert Note('C').calc_distance_to(Note('A')) == (6, 9)
        assert Note('C').calc_distance_to(Note('B')) == (7, 11)

        # some accidentals
        assert Note('Cb').calc_distance_to(Note('B#')) == (7, 11)
        assert Note('D#').calc_distance_to(Note('Gb')) == (4, 5)

        # more than an octave
        assert Note('G').calc_distance_to(Note('D')) == (5, 7)
        assert Note('D').calc_distance_to(Note('C')) == (7, 10)
        assert Note('B').calc_distance_to(Note('D')) == (3, 3)
        assert Note('F').calc_distance_to(Note('D')) == (6, 9)
