"""Interval Module"""
from .music import QUALITIES, INTERVALS, MAJOR, MINOR, AUG, DIM


class Interval:
    """Interval Class"""

    def __init__(self, quality, quantity):
        if quality not in QUALITIES:
            raise ValueError(
                "Quality should be one of [%s]. Got %s" % (QUALITIES, quality)
            )

        if quantity < 1 or quantity > 8:
            raise ValueError(
                "Qualitiy should be in range [0, 8]. Got %s" % quantity
            )

        self.quality = quality
        self.quantity = quantity
        self.name = "%s%s" % (quality, quantity)

        if self.name not in INTERVALS:
            raise ValueError(("Interval %s invalid. "
                              "Must be one of %s") %
                             (self.name, INTERVALS.keys()))

        (_, semitones) = INTERVALS[self.name]
        self.semitones = semitones

    @staticmethod
    def from_quantity_and_semitones(quantity, semitones):
        """Creates a new interval based on quantity and number of semitones."""
        for item, _ in INTERVALS.items():
            if item[-1] == str(quantity) and INTERVALS[item][1] == semitones:
                return Interval.from_string(item)

        raise LookupError("Combination of quantity and semitones is invalid.")

    @staticmethod
    def from_string(interval):
        """Creates a new Interval object from a string instead tuples."""
        if interval not in list(INTERVALS.keys()):
            raise ValueError(
                "Interval should be one of %s. Got %s" % (
                    INTERVALS.keys(),
                    interval
                )
            )

        quantity = int(interval[1:])
        quality = interval[:1]

        return Interval(quality, quantity)

    def invert(self):
        """Returns the complimentary interval for the current one."""
        new_quality = self.quality

        if self.quality == MAJOR:
            new_quality = MINOR
        elif self.quality == MINOR:
            new_quality = MAJOR
        elif self.quality == AUG:
            new_quality = DIM
        elif self.quality == DIM:
            new_quality = AUG

        new_quantity = 9 - self.quantity
        return Interval(new_quality, new_quantity)
