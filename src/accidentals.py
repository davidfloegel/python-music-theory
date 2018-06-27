"""Accidentals Module"""

import re
from itertools import chain
from .music import SHARP, DOUBLE_SHARP


class Accidentals:
    """Accidentals Class"""

    def __init__(self, accidentals=''):
        match = re.search('^([x,#]*|b*)$', accidentals)

        if match:
            split = list(accidentals)
            self.sanitised = self._sanitise(split)

            self.accidentals = accidentals
            self.value = self._calc_value()
        else:
            msg = ("Accidentals invalid. Allowed characters are [#, x, b]. "
                   "Got %s") % accidentals
            raise ValueError(msg)

    @classmethod
    def _sanitise(cls, accidentals_list):
        """
        Sanitise accidentals. Only needed when double SHARP 'x' is used.
        Turns [#, x] into [#, #, #] for easier calculations
        """
        if DOUBLE_SHARP in accidentals_list:
            accidentals_list[:] = [[SHARP, SHARP]
                                   if x == DOUBLE_SHARP
                                   else x for x in accidentals_list]
            accidentals_list = list(chain(*accidentals_list))

        return accidentals_list

    def _calc_value(self):
        """Calculate a + or - value for a given list of accidentals"""
        length = len(self.sanitised)
        if length == 0:
            return 0

        ind = 1 if self.sanitised[0] == SHARP else -1
        return ind * length
