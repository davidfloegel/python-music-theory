"""Key Signatures Test"""
import unittest
from nose.tools import assert_raises

from .keysignature import KeySignature

class KeySignatureTest(unittest.TestCase):
    """Key Signatures Test"""

    @classmethod
    def test_invalid_key_signature(cls):
        """Test if exceptions is thrown if key signature is invalid."""
        assert_raises(ValueError, KeySignature, 'M')
        assert_raises(ValueError, KeySignature, 'Gx')

    @classmethod
    def test_initialise_new_major_key(cls):
        """
        Test if key signature has been instantiated and has all the
        relevant properties
        """
        keysig = KeySignature('A')
        assert keysig.key == 'A'

        # notes in this key
        assert keysig.notes == ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']
        assert keysig.natural_notes == ['A', 'B', 'D', 'E']
        assert keysig.altered_notes == ['C#', 'F#', 'G#']

        # related keys
        assert keysig.relative_key == 'f#'
        assert keysig.parallel_key == 'a'
        assert keysig.dominant_key == 'E'
        assert keysig.subdominant_key == 'D'

    @classmethod
    def test_initialise_new_minor_key(cls):
        """Test initialising a new minor key"""
        keysig = KeySignature('f')
        assert keysig.key == 'f'

        # notes in this key
        assert keysig.notes == ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb']
        assert keysig.natural_notes == ['F', 'G', 'C']
        assert keysig.altered_notes == ['Ab', 'Bb', 'Db', 'Eb']

        # related keys
        assert keysig.relative_key == 'Ab'
        assert keysig.parallel_key == 'F'
        assert keysig.dominant_key == 'c'
        assert keysig.subdominant_key == 'bb'
