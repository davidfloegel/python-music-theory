"""Music Module"""

SHARP = '#'
DOUBLE_SHARP = 'x'
FLAT = 'b'

MAJOR = 'M'
MINOR = 'm'
PERFECT = 'P'
DIM = 'd'
AUG = 'A'

DEFAULT_OCTAVE = 4
DEFAULT_MIDI_VALUE = 0

""" NoteName: (NoteIndex on Keyboard, Note Value in Semitones) """
NOTES = {
    'C': (1, 0),
    'D': (2, 2),
    'E': (3, 4),
    'F': (4, 5),
    'G': (5, 7),
    'A': (6, 9),
    'B': (7, 11)
}

NOTE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

"""
List of all possible intervals.
"""
INTERVALS = {
    'P1': ('Perfect Unison', 0),
    'd2': ('Diminished 2nd', 0),
    'm2': ('Minor 2nd', 1),
    'A1': ('Augmented Unison', 1),
    'M2': ('Major 2nd', 2),
    'd3': ('Diminished 3rd', 2),
    'm3': ('Minor 3rd', 3),
    'A2': ('Augmented 2nd', 3),
    'M3': ('Major 3rd', 4),
    'd4': ('Diminished 4th', 4),
    'P4': ('Perfect 4th', 5),
    'A3': ('Augmented 3rd', 5),
    'd5': ('Diminished 5th', 6),
    'A4': ('Augmented 4th', 6),
    'P5': ('Perfect 5th', 7),
    'd6': ('Diminished 6th', 7),
    'm6': ('Minor 6th', 8),
    'A5': ('Augmented 5th', 8),
    'M6': ('Major 6th', 9),
    'd7': ('Diminished 7th', 9),
    'm7': ('Minor 7th', 10),
    'A6': ('Augmented 6th', 10),
    'M7': ('Major 7th', 11),
    'd8': ('Diminished Octave', 11),
    'A7': ('Augmented 7th', 12),
    'P8': ('Perfect Octave', 12)
}

"""
Set of qualities
"""
QUALITIES = (MAJOR, MINOR, PERFECT, AUG, DIM)

"""
Major Key with all the notes within that key.
Relative minor, parallel key, dominant and subdominant keys can be derived
from that.
"""
CIRCLE_OF_FIFTHS = {
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
    'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
    'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
    'Cb': ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'],
    'Gb': ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'],
    'Db': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
    'Ab': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
    'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
    'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
}
