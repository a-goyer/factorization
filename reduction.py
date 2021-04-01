from .precision_error import PrecisionError
from sage.modules.free_module_element import vector
from sage.matrix.constructor import matrix
from sage.matrix.special import identity_matrix



def REF(mat, *, transformation=False, pivots=False, prec_pivots={}):

    r"""
    Return a row echelon form of "mat".

    Note: this function is designed for BallField as base ring.

    The computed row echelon form is 'almost reduced': the pivots are set to 1
    and the coefficients below the pivots are set to 0 but the coefficients
    above the pivots may be nonzero.

    Some words about the correction of this function:
    Let (R, T, p) be the output for REF(mat, transformation=True, pivots=True).
    For any mat· in mat, there are R· in R and T· in T such that:
    i) for each j of p, R[p[j],j] = 1 and R[i,j] = 0 for i > p[j] (exactly),
    ii) R· = T· * mat· and T· is invertible,
    iii) the lenght of p cannot exceed the rank of mat·,
    iv) only the len(p) first rows of R do not contain the null row.
    Reversely, let mat· be fixed. If mat is precise enough, no PrecisionError
    is raised and the lenght of p is equal to the rank of mat·.

    Assumption: for p=prec_pivots, the len(p) first rows of mat satisfy i).


    INPUT:

     -- "mat"            -- an m×n matrix of balls
     -- "transformation" -- a boolean (optional, default: False)
     -- "pivots"         -- a boolean (optional, default: False)
     -- "prec_pivots"    -- a dictionary (optional, default: {})


    OUTPUT:

     -- "R" -- an m×n matrix of balls
     -- "T" -- an m×m matrix of balls (if 'transformation=True' is specified)
     -- "p" -- a dictionary (if 'pivots=True' is specified, more details below)

    The keys of the dictionary "p" are the indices of the columns which contain
    a pivot and p[j] is the corresponding row index.


    EXAMPLES:

    An example with a generic 3×3 matrix. ::

        sage: from diffop_factorization.reduction import REF
        sage: K = RealBallField(20)
        sage: mat = matrix(K, 3, [RR.random_element() for cpt in range(9)]); mat
        [ [-0.655408 +/- 6.67e-8]  [-0.134570 +/- 4.86e-7]   [0.150069 +/- 2.40e-7]]
        [ [-0.222183 +/- 3.23e-7]  [-0.833284 +/- 2.13e-7]   [0.885925 +/- 5.44e-8]]
        [ [-0.790008 +/- 1.47e-7] [-0.0786588 +/- 3.42e-8]   [0.146726 +/- 9.49e-8]]
        sage: R, T, p = REF(mat, transformation=True, pivots=True); R
        [                1.00000  [0.099567 +/- 4.54e-7] [-0.185727 +/- 8.63e-7]]
        [                      0                 1.00000   [-1.0413 +/- 1.48e-5]]
        [                      0                       0                 1.00000]
        sage: T*mat
        [  [1.00000 +/- 4.63e-6]  [0.099567 +/- 4.54e-7] [-0.185727 +/- 8.63e-7]]
        [          [+/- 4.65e-6]    [1.0000 +/- 8.31e-6]   [-1.0413 +/- 1.48e-5]]
        [          [+/- 1.95e-3]           [+/- 4.11e-4]     [1.000 +/- 5.21e-4]]
        sage: p
        {0: 0, 1: 1, 2: 2}

    An example with a singular 3×3 matrix. ::

        sage: from diffop_factorization.reduction import REF
        sage: K = RealBallField(20)
        sage: mat = random_matrix(QQ, 3, 3, algorithm='echelonizable', rank=2)
        sage: ran = matrix(K, 3, [RR.random_element() for i in range(9)])
        sage: mat = ~ran * mat * ran; mat
        [ [3.089 +/- 8.73e-4]  [-2.05 +/- 2.67e-3] [-1.466 +/- 7.17e-4]]
        [ [1.024 +/- 7.86e-4] [-10.81 +/- 3.26e-3] [-5.653 +/- 4.33e-4]]
        [[-1.204 +/- 1.78e-4]  [8.927 +/- 4.31e-4]  [4.718 +/- 3.11e-4]]
        sage: REF(mat)
        [             1.00000 [-0.664 +/- 5.83e-4] [-0.475 +/- 6.38e-4]]
        [                   0              1.00000  [0.510 +/- 3.73e-4]]
        [                   0                    0        [+/- 2.18e-3]]

    An example with a generic 3×4 matrix. ::

        sage: from diffop_factorization.reduction import REF
        sage: K = RealBallField(10)
        sage: mat =  matrix(K, 3, 4, [RR.random_element() for i in range(12)]); mat
        [[-0.794 +/- 2.56e-4]  [0.649 +/- 4.95e-4] [-0.109 +/- 1.70e-4]  [0.798 +/- 8.63e-5]]
        [[-0.645 +/- 3.14e-4] [-0.882 +/- 3.60e-4] [-0.555 +/- 4.51e-4] [-0.986 +/- 4.24e-4]]
        [ [0.298 +/- 5.29e-5]  [0.217 +/- 4.81e-4] [-0.521 +/- 1.37e-4]  [0.626 +/- 3.28e-4]]
        sage: REF(mat)
        [               1.00 [-0.82 +/- 6.85e-3] [0.137 +/- 8.34e-4] [-1.00 +/- 6.71e-3]]
        [                  0                1.00  [0.33 +/- 4.73e-3]    [1.2 +/- 0.0535]]
        [                  0                   0                1.00   [-0.5 +/- 0.0772]]

    An example with a generic 4×3 matrix. ::

        sage: from diffop_factorization.reduction import REF
        sage: K = RealBallField(20)
        sage: mat =  matrix(K, 4, 3, [RR.random_element() for i in range(12)]); mat
        [  [0.314239 +/- 3.15e-7]   [0.572433 +/- 2.10e-7]   [0.794824 +/- 9.85e-8]]
        [  [0.237214 +/- 1.11e-7]  [-0.579073 +/- 4.26e-7]   [0.444660 +/- 1.36e-7]]
        [  [0.565036 +/- 3.48e-7]   [0.938426 +/- 3.17e-7]  [-0.674036 +/- 1.86e-7]]
        [[-0.0756391 +/- 2.13e-8]  [-0.868542 +/- 2.49e-8]  [-0.827502 +/- 2.90e-7]]
        sage: R, T = REF(mat, transformation=True); R
        [               1.00000   [1.6608 +/- 3.04e-5] [-1.19291 +/- 7.88e-6]]
        [                     0                1.00000 [-0.74779 +/- 7.43e-6]]
        [                     0                      0                1.00000]
        [                     0                      0                      0]
        sage: T*mat
        [ [1.00000 +/- 4.68e-6]   [1.6608 +/- 3.04e-5] [-1.19291 +/- 7.88e-6]]
        [         [+/- 4.09e-6]   [1.0000 +/- 9.39e-6] [-0.74779 +/- 7.43e-6]]
        [         [+/- 7.08e-6]          [+/- 2.07e-5]    [1.000 +/- 1.65e-5]]
        [         [+/- 1.86e-5]          [+/- 4.95e-5]          [+/- 4.17e-5]]
        sage: T.det()
        [1.23 +/- 5.18e-3]

    """

    m, n, C = mat.nrows(), mat.ncols(), mat.base_ring()
    T = identity_matrix(C, m)
    p = prec_pivots.copy()
    r = len(p)

    for j in p:
        col = T * vector(mat[:,j])
        for i in range(r, m):
            T[i] = [T[i,k] - col[i]*T[p[j],k] for k in range(m)]

    for j in range(n):

        if not j in p:
            r, col = len(p), T * vector(mat[:,j])
            i = max((l for l in range(r, m) if col[l].is_nonzero()), \
            key=lambda l: col[l].below_abs(), default=None)

            if i is not None:
                p[j] = r
                T[i], T[r], col[i], col[r] = T[r], T[i], col[r], col[i]
                T[r] = [T[r,k]/col[r] for k in range(m)]
                for l in range(r+1, m):
                    T[l] = [T[l,k] - col[l]*T[r,k] for k in range(m)]

    R = T * mat
    for j in p:
        R[p[j],j] = 1
        for i in range(p[j]+1, m): R[i,j] = 0

    if transformation:
        if T.det().contains_zero():
            raise PrecisionError("Cannot compute an invertible matrix.")
        if pivots: return R, T, p
        else: return R, T
    if pivots: return R, p
    else: return R


def orbit(Mats, vec, *, transition=False):

    r"""
    Return a basis of the smallest subspace containing "vec" and invariant under
    (the action of) the matrices of "Mats".

    Note: this function is designed for BallField as base ring.

    Some words about the correction of this function:
    Let (b, T) be the output for orbit(Mats, vec, transition=True). For any
    selection [mat1·, ..., matk·] in Mats = [mat1, ..., matk] and any vec· in
    vec, there are a selection [b1·, ..., bs·] in b = [b1, ..., bs] and a
    selection [T1·, ..., Ts·] in T = [T1, ..., Ts] such that:
    i) the subspace spanned by b1·, ..., bs· is contained in the smallest
    subspace containing vec· and invariant under mat1·, ..., matk·,
    ii) the vectors b1·, ..., bs· are linearly independent,
    iii) for each i, bi· = Ti·*vec· and Ti· is polynomial in mat1·, ..., matk·.
    Reversely, let [mat1·, ..., matk·] and vec· be fixed. If Mats and vec are
    precise enough, no PrecisionError is raised and there is selection
    [b1·, ..., bs·] which is a basis of the smallest subspace containing vec·
    and invariant under mat1·, ..., matk·.

    In particular, if b has lenght the dimension, this proves that whatever the
    selection [mat1·, ..., matk·] in Mats and whatever vec· in vec, the smallest
    subspace containing vec· and invariant under mat1·, ..., matk· is the entire
    space.


    INPUT:

     -- "Mats"       -- a list of n×n matrices
     -- "vec"        -- a vector of size n
     -- "transition" -- a boolean (optional, default: False)

    OUTPUT:

     -- "b" -- a list of vectors of size n
     -- "T" -- a list of n×n matrix


    EXAMPLES:

    An example with one matrix. ::

        sage: from diffop_factorization.reduction import orbit
        sage: mat = matrix(RBF, [[1, 1, 0], [0, 1, 1], [0, 0, 1]])
        sage: u, v, w = list(identity_matrix(RBF, 3))
        sage: ran = MatrixSpace(RR, 3).random_element().change_ring(RBF)
        sage: u, v, w, mat = ~ran * u, ~ran * v, ~ran * w, ~ran * mat * ran
        sage: len(orbit([mat], u)), len(orbit([mat], v)), len(orbit([mat], w))
        (1, 2, 3)
        sage: b, T = orbit([mat], v, transition=True)
        sage: b[0], T[0]*v
        ((1.000000000000000, [1.630667151553 +/- 2.48e-13], [1.710645064117 +/- 4.32e-13]),
         ([1.00000000000 +/- 2.41e-13], [1.630667151553 +/- 2.48e-13], [1.710645064117 +/- 4.32e-13]))
        sage: b[1], T[1]*v
        ((0, 1.000000000000000, [5.2453796816 +/- 5.24e-11]),
         ([+/- 5.79e-12], [1.0000000000 +/- 1.53e-11], [5.2453796816 +/- 5.25e-11]))

    An example with two matrices. ::

        sage: from diffop_factorization.reduction import orbit
        sage: mat1 = matrix(CBF, [[0, 0, 1], [0, 0, 0], [0, 0, 0]])
        sage: mat2 = matrix(CBF, [[0, 0, 0], [0, 0, 1], [0, 0, 0]])
        sage: vec = vector(CBF, [0, 0, 1])
        sage: ran = MatrixSpace(CC, 3).random_element().change_ring(CBF)
        sage: vec, mat1, mat2 =  ~ran * vec, ~ran * mat1 * ran, ~ran * mat2 * ran
        sage: len(orbit([mat1], u)), len(orbit([mat1, mat2], u))
        (2, 3)

    """

    n, C = len(vec), vec.base_ring()

    b, S, p = REF(matrix(vec), transformation=True, pivots=True)
    if transition: T = [S[0,0]*identity_matrix(C, n)]

    if len(p)==0: # case where vec contains the null vector
        if transition: return [], []
        else: return []

    r, new = 1, range(0, 1)
    while len(new) > 0 and r < n:

        b = b.stack(matrix([mat*vector(b[i]) for mat in Mats for i in new]))
        if transition:
            T.extend([mat*T[i] for mat in Mats for i in new])

        if transition:
            b, S, p = REF(b, transformation=True, pivots=True, prec_pivots = p)
        else:
            b, p = REF(b, pivots=True, prec_pivots = p)

        new = range(r, len(p))
        b = b.matrix_from_rows(range(len(p)))
        if transition:
            T[r:] = [sum(S[i,j]*Tj for j, Tj in enumerate(T)) for i in new]
        r = len(p)

    if transition: return list(b), T
    else: return list(b)



def generated_algebra(Mats):

    r"""
    Return a basis of the (unitary) algebra generated by the matrices of "Mats".

    Note: this function is designed for BallField as base ring.
    Let b be the output for generated_algebra(Mats). For any selection
    [mat1·, ..., matk·] in Mats = [mat1, ..., matk], there is a selection
    [b1·, ..., bs·] in b = [b1, ..., bs] such that:
    i) the subspace spanned by b1·, ..., bs· is contained in the algebra
    generated by mat1·, ..., matk·,
    ii) the matrices b1·, ..., bs· are linearly independent,
    iii) for each i, bi· is polynomial in mat1·, ..., matk·.
    Reversely, let [mat1·, ..., matk·] be fixed. If Mats is precise enough, no
    PrecisionError is raised and there is selection [b1·, ..., bs·] in the
    output which is a basis of the algebra generated by mat1·, ..., matk·.

    In particular, if b has lenght n×n where n is the dimension, this proves
    that whatever the selection [mat1·, ..., matk·] in Mats, the matrices
    mat1·, ..., matk· generate the entire algebra of matrices.

    INPUT:

     -- "Mats" -- a list of n×n matrices

    OUTPUT:

     -- "b" -- a list of n×n matrices


    EXAMPLES::

        sage: from diffop_factorization.reduction import generated_algebra
        sage: n, C = 4, ComplexBallField(100)
        sage: mat1 = MatrixSpace(CC, n).random_element().change_ring(C)
        sage: mat2 = MatrixSpace(CC, n).random_element().change_ring(C)
        sage: len(generated_algebra([mat1, mat2]))
        16
        sage: len(generated_algebra([mat1**2, mat1**3]))
        4

    """


    mat = Mats[0]
    n, C = mat.nrows(), mat.base_ring()

    b, p = REF(matrix([mat.list() for mat in Mats]), pivots=True)
    r = len(p)
    b = b.matrix_from_rows(range(r))
    new = range(0, r)

    while len(new) > 0 and r < n**2:

        b = b.stack(matrix([(matrix(n,b[i])*matrix(n,b[j])).list() for i in range(r) for j in new]))
        b, p = REF(b, pivots=True, prec_pivots = p)

        new = range(r, len(p))
        r = len(p)
        b = b.matrix_from_rows(range(r))

    return list(b)
