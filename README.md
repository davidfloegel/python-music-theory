# Music Theory

> A python 3.6 library to solve music theory related questions.

[![CircleCI](https://circleci.com/gh/davidfloegel/python-music-theory/tree/master.svg?style=svg)](https://circleci.com/gh/davidfloegel/python-music-theory/tree/master)

## ToDos

- Write documentation on existing code and theory
- Calculate Scales
- Chord Progressions

## Purpose

This library was written to power a music theory / ear training app I'm currently developing with [@cle-ment](https://www.github.com/cle-ment).

## Installation

> @TODO  
> This library will soon be available for installation via `pip` or similar commands.

## API Overview

We're trying to make this libraries API as software agnostic as possible so that it can easily be translated into different languages.

### Notes

#### Instantiating a new Note
Instantiating a new note is as easy as calling the `Note` constructor and passing in your note name. The note constructor will look for the actual name, any accidentals and the octave which will default to the default octave 4.

```python
# a simple note
simple_note = Note('C')

# a note with accidentals
note_with_accidental_1 = Note('Eb')
note_with_accidental_2 = Note('Ab')
note_with_accidental_2 = Note('F#')

# a note in a specific octave
note_in_octave = Note('G3')

# a note with accidentals and an octave
complex_note = Note('Abb5')
```

#### Attributes
You have access to a few different attributes once a note has been created. Let's take it from the example of the note `Abb5`

##### note.letter
The letter is the actual note name without any modifiers. In this case `A`

##### note.accidentals
The accidentals will hand you an instance of the `Accidentals` class which contains all the accidentals attributes and few helpers.

##### note.octave
Returns the octave of the note as int. In this case `5`

##### note.midi_value
Returns the calculated midi value for this note. In this case `79`

##### note.easy_notation
The `easy_notation` attribute simplifies the way the note is written if it has multiple accidentals. The note `Abb` is technically speaking a `G` so the `easy_notation` property will return `G5`

#### Operators

##### ==
The `==` operator checks if note B is of the same (midi) value or the enharmonic equivalent of note A.  Have a look at this test excerpt.

```python
note_a = Note('C#')
note_b = Note('Db')
note_c = Note('D')

assert note_a == note_b # true
assert note_a == note_c # false
```

##### note.is_same
The `is_same` method checks note equality based on name *and* midi value. In other words, it has to be the exact same note. The enharmonic equivalent would not pass.

```python
note_a = Note('C#')
note_b = Note('Db')
note_c = Note('C#')

assert note_a.is_same(note_b) # false
assert note_a.is_same(note_c) # true
```

--------


### Intervals

```python
# create a new interval
interval = Interval('M', 3)
interval_from_string = Interval('P4')

# invert an interval
interval = Interval('P4')
inverted = interval.invert()
inverted.name = 'P5'

# adding an interval to a note
note = Note('C')
target = note + Interval.from_string('P4')
target.name = 'F'

note = Note('E')
target = note - Interval.from_string('M3')
target.name = 'C'

# calculate interval between two notes
root = Note('G')
target = Note('C')
interval = root.minus_note(target)
interval.name = 'P5'

root = Note('F')
target = Note('A')
interval = root.minus_note(target)
interval.name = 'M3'
```

### Key Signatures

```
keysig = KeySignature('A') # A major

keysig.notes == ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']
keysig.natural_notes == ['A', 'B', 'D', 'E']
keysig.altered_notes == ['C#', 'F#', 'G#']

# related keys
keysig.relative_key == 'f#'
keysig.parallel_key == 'a'
keysig.dominant_key == 'E'
keysig.subdominant_key == 'D'


# minor keys
keysig = KeySignature('e') # E minor
```

## Unit Tests

You can find unit tests next to the actual implementation.
Run `make test` on your terminal to run the tests.

## Contribution

I'm happy for every contribution to this project, may it be new features, bug fixes or code improvements. Here's a few guide lines:
- If you want to contribute, create a branch (such as `fix/what-is-fixed` or `improve/what-is-improved` or `feature/name`) from `dev` and create a PR.
- Please add tests. If it's not a small change I won't accept your PR without tests.
- Make sure the CircleCI integration passes (currently `make lint` and `make test`)
- Write a meaningful commit message. No one wants to see `wip` - forgive me for doing it myself

## License

[Read](https://github.com/davidfloegel/python-music-theory/blob/master/LICENSE)

Copyright (c) 2018 - present, David Floegel
