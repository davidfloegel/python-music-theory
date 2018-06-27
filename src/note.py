"""Note Module"""

import re
from .music import SHARP, FLAT, DEFAULT_OCTAVE, NOTES, NOTE_KEYS

from .accidentals import Accidentals
from .interval import Interval


class Note:
    """Note Class"""

    def __init__(
            self,
            name,
            octave=DEFAULT_OCTAVE
    ):
        self.name = name

        # Regex for note name syntax
        match = re.search('^([A-G])([#xb]*)([1-8]?)$', name)

        if match:
            self.letter = match.group(1)
            self.accidentals = Accidentals(match.group(2) or '')
            self.octave = int(match.group(3)) if match.group(3) \
                else octave
            self.midi_value = self._calc_midi_val()
            self.easy_notation = self._calc_easy_notation()
        else:
            raise ValueError(
                "Note Format Invalid. Must be [A-G]([#xb]*)([1-8]?). Got %s",
                self.name
            )

    def __eq__(self, note):
        """Returns true if two NOTES are the same (enharmonically)"""
        return self.midi_value == note.midi_value

    def __add__(self, interval):
        """Returns a new note that has the given interval added"""
        return self._add_or_sub_interval(interval, +1)

    def __sub__(self, interval):
        """Returns a new note that has the given interval subtracted"""
        return self._add_or_sub_interval(interval, -1)

    @staticmethod
    def from_index(index):
        """Find a note by their index. Returns the note name or None"""
        for item, _ in NOTES.items():
            if NOTES[item][0] == index:
                return Note(item)
        return None

    @staticmethod
    def from_semitones(semitones):
        """Find a note by their index. Returns the note name or None"""
        for item, _ in NOTES.items():
            if NOTES[item][1] == semitones:
                return Note(item)
        return None

    def _calc_easy_notation(self):
        """
        Get the easy notation for this note if applicable. For example:
        Cb:B, Abb:G, E#:F
        """
        match = re.search('^([C,F]b+|[B,E][#x]+|[A-G](#x+|x+|#{2,}|b{2,}))$', self.name)

        if match:
            letter = self.letter
            (_, semitones) = NOTES[letter]
            octave = self.octave
            accidental_val = self.accidentals.value

            # calculate the new position of the note by adding the accidental value of current note
            new_note_pos = semitones + accidental_val

            # check if a note exists
            new_note = Note.from_semitones(new_note_pos)

            if new_note is not None:
                return new_note

            # is the current note a C or B ? if yes, they need special handling
            add_accidentals = ''
            adjust_note_pos_by = -1 if accidental_val > 0 else 1

            if letter in ['C', 'B']:
                octave += -1 if letter == 'C' else 1
                new_note_pos = 11 if letter == 'C' else 0

                if abs(accidental_val) > 2:
                    new_note_pos += accidental_val + (1 if accidental_val < 0 else - 1)

                accidental_val += adjust_note_pos_by

                if accidental_val % 2 != 0:
                    add_accidentals = SHARP if accidental_val > 0 else FLAT
            else:
                new_note_pos += adjust_note_pos_by
                if accidental_val != 0:
                    add_accidentals = SHARP if accidental_val > 0 else FLAT

            # note doesn't exist, try adjusting semitones
            new_note = Note.from_semitones(new_note_pos)

            return Note(new_note.name + add_accidentals, octave)
        else:
            return None

    def _calc_midi_val(self):
        """Calculates the midi value of a note"""
        (_, note_value) = NOTES[self.letter]
        note_value += self.accidentals.value
        note_value += (self.octave + 1) * 12
        return note_value

    def is_same(self, note):
        """Returns true if two NOTES are exactly the same"""
        return self == note and self.name == note.name

    def _add_or_sub_interval(self, interval, direction):
        """
        Private method to add or subtract an interval from the current note.
        Parameters are the interval and a direction (+1 = add / -1 = sub)
        """
        is_add = direction == +1

        (curr_note_idx, _) = NOTES[self.letter]
        quantity = interval.quantity - 1
        new_note_idx = curr_note_idx + quantity \
            if is_add \
            else curr_note_idx - quantity

        octave_offset = 0

        if is_add and new_note_idx > 7:
            octave_offset += 1
            new_note_idx -= 7

        if not is_add and new_note_idx < 1:
            octave_offset -= 1
            new_note_idx += 7

        new_note_name = NOTE_KEYS[new_note_idx - 1]
        new_note_unadj = Note(new_note_name + str(self.octave + octave_offset))

        if is_add:
            accidental_adjustment = interval.semitones \
                - (new_note_unadj.midi_value - self.midi_value)
        else:
            accidental_adjustment = (
                self.midi_value - new_note_unadj.midi_value
            ) - interval.semitones

        accidentals = ''
        if accidental_adjustment > 0:
            accidentals = SHARP * accidental_adjustment
        elif accidental_adjustment < 0:
            accidentals = FLAT * abs(accidental_adjustment)

        return Note(new_note_name + accidentals, self.octave + octave_offset)

    def minus_note(self, target):
        """Returns the interval between two NOTES."""
        root_accidentals = self.accidentals
        target_accidentals = target.accidentals

        # check if interval is descending or ascending
        is_desc = self.midi_value > target.midi_value if \
            self.octave == target.octave else self.octave > target.octave

        # calculate the distance between two NOTES to determine interval type
        (quantity, semitones) = self.calc_distance_to(target)

        if is_desc:
            # if target note is exactly one octave (12 steps) below root
            # note we have an octave and don't need to adjust values
            if not self.midi_value == target.midi_value + 12:
                quantity = 9 - quantity
                semitones = 12 - semitones

            semitones += self._adjust_accidentals(root_accidentals, SHARP)
            semitones += self._adjust_accidentals(target_accidentals, FLAT)
        else:
            semitones += self._adjust_accidentals(root_accidentals, FLAT)
            semitones += self._adjust_accidentals(target_accidentals, SHARP)

        return Interval.from_quantity_and_semitones(quantity, semitones)

    def calc_distance_to(self, target):
        """
        Returns the distance between two NOTES and the actual semitones
        This only calculates the semitones between base NOTES, no accidentals
        are considered.
        """
        note_names = NOTE_KEYS
        root_idx = note_names.index(self.letter)
        target_idx = note_names.index(target.letter)

        (_, root_semitones) = NOTES[self.letter]
        (_, target_semitones) = NOTES[target.letter]

        if target_idx == root_idx and self.octave == target.octave:
            return 1, 0
        elif target_idx > root_idx:
            return (
                target_idx - root_idx + 1,
                target_semitones - root_semitones
            )

        return (
            (7 - root_idx) + target_idx + 1,
            (12 - root_semitones) + target_semitones
        )

    @classmethod
    def _adjust_accidentals(cls, accidentals, compare_with):
        if not accidentals.value == 0:
            first_accident = accidentals.accidentals[:1]
            increase = first_accident == compare_with
            value = abs(accidentals.value)

            return value if increase else value * -1

        return 0
