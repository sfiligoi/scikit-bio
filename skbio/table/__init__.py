r"""Data Table (:mod:`skbio.table`)
==================================

.. currentmodule:: skbio.table

This module provides support for interaction with data tables in the Biological
Observation Matrix (BIOM) format.

Please refer to the `BIOM documentation <https://biom-format.org/>`__ for the
instructions on working with BIOM tables.


BIOM table
----------

.. autosummary::
   :toctree: generated/

   Table


Example data
^^^^^^^^^^^^
.. autosummary::
   :toctree: generated/

   example_table

Data Augmentation
-----------------

.. autosummary::
   :toctree: generated/

   phylomix
   compositional_cutmix
   mixup
   aitchison_mixup

"""  # noqa: D205, D415

# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------

from skbio.table._base import Table, example_table
from skbio.table._augment import phylomix, compositional_cutmix, aitchison_mixup, mixup

__all__ = [
    "Table",
    "example_table",
    "phylomix",
    "compositional_cutmix",
    "aitchison_mixup",
    "mixup",
]
