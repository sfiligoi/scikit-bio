# ----------------------------------------------------------------------------
# Copyright (c) 2021-2021, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np

from ._cutils import vec_fma_cy, distmat_reorder_cy, distmat_reorder_condensed_cy

def vec_fma_buf(in_vec, mul, add, out_vec):
    """
    Compute out_vec = mul*in_vec + add

    Parameters
    ----------
    in_mat : 1D array_like
        Input array
    mul: real
        Multiplication factor
    add: real
        Addition
    out_mat : 1D array_like
        Output array, safe to use in_vec, too
    """
    vec_fma_cy(in_vec, mul, add, out_vec)

def vec_fma(in_vec, mul, add):
    """
    Compute out_vec = mul*in_vec + add

    Parameters
    ----------
    in_mat : 1D array_like
        Input array
    mul: real
        Multiplication factor
    add: real
        Addition

    Return
    ------
    out_mat : 1D array_like
        Output array
    """
    out_vec = np.empty(in_vec.shape, in_vec.dtype)
    vec_fma_cy(in_vec, mul, add, out_vec)
    return out_vec

def distmat_reorder_buf(in_mat, reorder_vec, out_mat, validate=False):
    """
    Reorder the rows and columns of a distance matrix
    given a reorder vector.
    Not all of the columns need to be used.

    For example:
     [ [0, 1, 2, 3] ,
       [1, 0, 4, 5] ,
       [2, 4, 0, 6] ,
       [3, 5, 6, 0] ]
     with
     [1,0,3,2]
     will result in
     [ [0, 1, 5, 4] ,
       [1, 0, 3, 2] ,
       [5, 3, 0, 6] ,
       [4, 2, 6, 0] ]

    Parameters
    ----------
    in_mat : 2D array_like
        Distance matrix
    reorder_vec : 1D_array_like
        List of permutation indexes
    out_mat : 2D array_like
        Output, Distance matrix,
        must be in c_order and same size as reorder_vec
    validate: boolean
        Optional, if True, validate reorder_vec content, detaults to False
    """
    np_reorder = np.asarray(reorder_vec, dtype=np.long)
    if validate:
        maxsize = in_mat.shape[0]
        bad_cnt = np.where((np_reorder < 0) or (np_reorder >= maxsize))[0].size
        if bad_cnt > 0:
            raise ValueError("Invalid reorder_vec")

    if not in_mat.flags.c_contiguous:
        in_mat = np.asarray(in_mat, order='C')

    distmat_reorder_cy(in_mat, np_reorder, out_mat)


def distmat_reorder(in_mat, reorder_vec, validate=False):
    """
    Reorder the rows and columns of a distance matrix
    given a reorder vector.
    Not all of the columns need to be used.

    For example:
     [ [0, 1, 2, 3] ,
       [1, 0, 4, 5] ,
       [2, 4, 0, 6] ,
       [3, 5, 6, 0] ]
     with
     [1,0,3,2]
     will result in
     [ [0, 1, 5, 4] ,
       [1, 0, 3, 2] ,
       [5, 3, 0, 6] ,
       [4, 2, 6, 0] ]

    Parameters
    ----------
    in_mat : 2D array_like
        Distance matrix, must be in c_order
    reorder_vec : 1D_array_like
        List of permutation indexes
    validate: boolean
        Optional, if True, validate reorder_vec content, detaults to False

    Returns
    -------
    out_mat : 2D array_like
        Distance matrix
    """
    np_reorder = np.asarray(reorder_vec, dtype=np.long)
    if validate:
        maxsize = in_mat.shape[0]
        bad_cnt = np.where((np_reorder < 0) or (np_reorder >= maxsize))[0].size
        if bad_cnt > 0:
            raise ValueError("Invalid reorder_vec")

    if not in_mat.flags.c_contiguous:
        in_mat = np.asarray(in_mat, order='C')

    out_mat = np.empty([np_reorder.size, np_reorder.size], in_mat.dtype)
    distmat_reorder_cy(in_mat, np_reorder, out_mat)
    return out_mat

def distmat_reorder_condensed(in_mat, reorder_vec, validate=False):
    """
    Reorder the rows and columns of a distance matrix
    given a reorder vector.
    Not all of the columns need to be used.

    For example:
     [ [0, 1, 2, 3] ,
       [1, 0, 4, 5] ,
       [2, 4, 0, 6] ,
       [3, 5, 6, 0] ]
     with
     [1,0,3,2]
     will result in
     [ 1, 5, 4 , 3, 2, 6 ]

    Parameters
    ----------
    in_mat : 2D array_like
        Distance matrix, must be in c_order
    reorder_vec : 1D_array_like
        List of permutation indexes
    validate: boolean
        Optional, if True, validate reorder_vec content, detaults to False

    Returns
    -------
    out_mat_condensed : 1D array_like
        Condensed distance matrix
    """
    np_reorder = np.asarray(reorder_vec, dtype=np.long)
    if validate:
        maxsize = in_mat.shape[0]
        bad_cnt = np.where((np_reorder < 0) or (np_reorder >= maxsize))[0].size
        if bad_cnt > 0:
            raise ValueError("Invalid reorder_vec")

    if not in_mat.flags.c_contiguous:
        in_mat = np.asarray(in_mat, order='C')

    out_mat_condensed = np.empty([np.long(((np_reorder.size-1)*np_reorder.size)/2)], in_mat.dtype)
    distmat_reorder_condensed_cy(in_mat, np_reorder, out_mat_condensed)
    return out_mat_condensed

class PearsonPermuttable:
    def __init__(self, x, y):
        # mean does not change on permutation
        self.xmean = x.mean()

        xm = x - self.xmean

        # norm does not change on permutation
        self.normxm = np.linalg.norm(xm)

        self.xm_normalized = xm/self.normxm
        del xm

        self.ymean = y.mean()
        ym = y - self.ymean
        self.normym = np.linalg.norm(ym)
        self.ym_normalized = ym/self.normym
        del ym

        threshold = 1e-13
        if ((self.normxm < threshold*abs(self.xmean)) or 
            (self.normym < threshold*abs(self.ymean))):
            # If all the values in x (likewise y) are very close to the mean,
            # the loss of precision that occurs in the subtraction xm = x - xmean
            # might result in large errors in r.
            warnings.warn(RuntimeWarning("An input array is nearly constant"))


    def compute(self):
        r = np.dot(self.xm_normalized, self.ym_normalized)

        # Presumably, if abs(r) > 1, then it is only some small artifact of
        # floating point arithmetic.
        r = max(min(r, 1.0), -1.0)

        return r

    def updatex(self, x):
        # xmean and normxm should not have changed, as it is just a permutation
        self.xm_normalized = vec_fma(x, 1.0/self.normxm, -self.xmean/self.normxm)

        return self


