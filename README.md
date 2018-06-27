# Music Theory

> A python 3.6 library to solve music theory related questions.

[![CircleCI](https://circleci.com/gh/davidfloegel/python-music-theory/tree/master.svg?style=svg)](https://circleci.com/gh/davidfloegel/python-music-theory/tree/master)

## ToDos

- Write documentation on existing code and theory
- Calculate Scales
- Chord Progressions

## Purpose

This library was written to power a music theory / ear training app I'm currently developing with [@cle-ment](https://www.github.com/cle-ment).

## Install

> @TODO  
> This library will soon be available for installation via `pip` or similar commands.

## Usage

### Notes

```python
note1 = Note('C')
note2 = Note('Eb')
note3 = Note('A#')
note4 = Note('Gbb')
note5 = Note('Ax)

note6 = Note('C5')
note7 = Note('Abbb3')

# easy notation (enharmonic equivalent)
note7.easy_notation.name = 'Gb3'

# is note enharmonic equivalent?
Note('C#') == Note('Db') => true

# is note the exact same?
Note('C#').is_same(Note('Db')) => false
Note('C#').is_same(Note('C#')) => true
```

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
