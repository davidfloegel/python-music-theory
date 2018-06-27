"""Key Signature Module"""
import re

from .music import CIRCLE_OF_FIFTHS
from .accidentals import Accidentals
from .interval import Interval
from .note import Note


class KeySignature:
    """Key Signature Class"""

    def __init__(self, key):
        self.key = key

        # Regex for key signature syntax
        match = re.search('^([a-gA-G])([#b]?)$', key)

        if match:
            self.letter = match.group(1)
            self.accidentals = Accidentals(match.group(2) or '')
            self.is_minor = self.letter.islower()
            self.tonic = Note(key.upper())
        else:
            raise ValueError(
                "Key Signature Invalid. Must be [a-gA-G]([#b]?). Got %s",
                self.key
            )

        notes = self._get_key_notes()
        self.notes = notes
        self.natural_notes = list(filter(lambda note: len(note) == 1, notes))
        self.altered_notes = list(filter(lambda note: len(note) > 1, notes))

        # calculate relative minor, parallel, dominant and subdominant key
        self.relative_key = self._calc_relative_key()
        self.parallel_key = self._calc_parallel_key()
        self.dominant_key = self._calc_dominant_key()
        self.subdominant_key = self._calc_subdominant_key()

    def _get_key_notes(self):
        """
        Get the correct notes for this key. If it's a minor key we need to get
        the correct major key (minor 3rd up) and rotate the notes to start on
        the correct note.
        """
        if self.is_minor:
            major = self.tonic + Interval.from_string("m3")
            notes = CIRCLE_OF_FIFTHS[major.name]
            return notes[5:] + notes[:5]

        return CIRCLE_OF_FIFTHS[self.key]

    def _calc_relative_key(self):
        """Calculate the relative key which is a minor 3rd below / above"""
        min3 = Interval.from_string("m3")
        target = self.tonic + min3 if self.is_minor else self.tonic - min3
        return target.name if self.is_minor else target.name.lower()

    def _calc_parallel_key(self):
        """Calculate the parallel key."""
        target = self.letter.upper() if self.is_minor else self.letter.lower()
        return target + self.accidentals.accidentals

    def _calc_dominant_key(self):
        """Calculate dominant key. Perfect 5th above tonic of this key"""
        target = self.tonic + Interval.from_string("P5")
        return target.name.lower() if self.is_minor else target.name

    def _calc_subdominant_key(self):
        """Calculate subdominant key. Perfect 4th above tonic of this key"""
        target = self.tonic + Interval.from_string("P4")
        return target.name.lower() if self.is_minor else target.name
