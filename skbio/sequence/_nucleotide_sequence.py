# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
from future.utils import with_metaclass

import re
from abc import ABCMeta, abstractproperty

from skbio.sequence import SequenceError
from skbio.util import classproperty
from skbio.util._misc import MiniRegistry
from ._iupac_sequence import IUPACSequence


class NucleotideSequence(with_metaclass(ABCMeta, IUPACSequence)):
    """Base class for nucleotide sequences.

    A `NucleotideSequence` is a `Sequence` with additional methods
    that are only applicable for nucleotide sequences, and containing only
    characters used in the IUPAC DNA or RNA lexicon.

    See Also
    --------
    Sequence

    Notes
    -----
    All uppercase and lowercase IUPAC DNA/RNA characters are supported.

    """

    @abstractproperty
    @classproperty
    def complement_map(cls):
        """Return the mapping of characters to their complements.

        Returns
        -------
        dict
            Mapping of characters to their complements.

        Notes
        -----
        Complements cannot be defined for a generic `NucleotideSequence`
        because the complement of 'A' is ambiguous.
        `NucleotideSequence.complement_map` will therefore be the empty dict.
        Thanks, nature...

        """
        pass

    def complement(self, reverse=False):
        """Return the complement of the `NucleotideSequence`

        Returns
        -------
        NucelotideSequence
            The complement of `self`. Specific type will be the same as
            ``type(self)``.

        Raises
        ------
        skbio.sequence.SequenceError
            If a character is present in the `NucleotideSequence` that is not
            in `self.complement_map`.

        See Also
        --------
        reverse_complement
        complement_map

        Notes
        -----
        The type, id, description, and quality scores of the result will be the
        same as `self`.

        """
        result = []
        complement_map = self.complement_map
        seq_iterator = reversed(self) if reverse else self
        for base in seq_iterator:
            # TODO fix me!
            base = str(base)
            try:
                result.append(complement_map[base])
            except KeyError:
                raise SequenceError(
                    "Don't know how to complement base %s. Is it in "
                    "%s.complement_map?" % (base, self.__class__.__name__))

        quality = self.quality
        if self._has_quality() and reverse:
            quality = self.quality[::-1]

        return self._to(sequence=''.join(result), quality=quality)

    def is_reverse_complement(self, other):
        """Return True if `other` is the reverse complement of `self`

        Returns
        -------
        bool
            `True` if `other` is the reverse complement of `self` and `False`
            otherwise.

        Raises
        ------
        skbio.sequence.SequenceError
            If a character is present in `other` that is not in the
            `self.complement_map`.

        See Also
        --------
        reverse_complement

        """
        return other.reverse_complement()._string == self._string

    def reverse_complement(self):
        """Return the reverse complement of the `NucleotideSequence`

        Returns
        -------
        NucelotideSequence
            The reverse complement of `self`. Specific type will be the same as
            ``type(self)``.

        Raises
        ------
        skbio.sequence.SequenceError
            If a character is present in the `NucleotideSequence` that is not
            in `self.complement_map`.

        See Also
        --------
        complement
        complement_map
        is_reverse_complement

        Notes
        -----
        The type, id, and description of the result will be the same as `self`.
        If quality scores are present, they will be reversed and included in
        the resulting biological sequence.

        """
        return self.complement(reverse=True)
    rc = reverse_complement

    @property
    def _motifs(self):
        return _motifs

_motifs = MiniRegistry()

def _find_runs(sequence, chars_to_find, min_length, allow_gaps):
    acceptable = re.escape(''.join(sequence.gap_chars)) if allow_gaps else ''
    pat = '([%s%s]{%d,})' % (chars_to_find, acceptable, min_length)
    for index in sequence.slices_from_regex(pat):
        if allow_gaps:
            if len(sequence) - sequence[index].gaps().sum() >= min_length:
                yield index
        else:
            yield index

@_motifs("purine-run")
def _motif_purine_run(sequence, min_length, allow_gaps):
    return _find_runs(sequence, "AG", min_length, allow_gaps)

@_motifs("pyrimidine-run")
def _motif_pyrimidine_run(sequence, min_length, allow_gaps):
    return _find_runs(sequence, "CTU", min_length, allow_gaps)

# Leave this at the bottom
_motifs.interpolate(NucleotideSequence, "find_motifs")
