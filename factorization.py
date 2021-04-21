from .precision_error import PrecisionError
from .useful_functions import customized_accuracy
from .invariant_subspace import InvSub
from .complex_optimistic_field import ComplexOptimisticField
from .guessing import hp_approx
from ore_algebra.analytic import monodromy_matrices
from sage.rings.power_series_ring import PowerSeriesRing
from sage.rings.real_mpfr import RealField

Radii = RealField(30)

def right_factor(L, prec=500, T=None):

    r"""
    Return a nontrivial right-hand factor of the linear differential operator L
    or None if there is none.
    """

    OA = L.parent()
    z, Dz = L.base_ring().gen(), OA.gen()

    z0 = 0
    while z0 in L.singularities():
        z0 += 1
    L = OA(L.annihilator_of_composition(z + z0))

    p = prec
    success = False
    while not success:
        eps = Radii.one() >> p
        try:
            mono = monodromy_matrices(L, 0, eps=eps)
            if 4*min(customized_accuracy(mat.list()) for mat in mono)<3*prec:
                p = 2*p
            else:
                success = True
        except ZeroDivisionError:
            p = 2*p

    try:
        V = InvSub(mono)
    except PrecisionError:
        return right_factor(L, prec=2*prec)

    if V is None:
        return None

    d = len(V)
    C = ComplexOptimisticField(prec, eps = Radii.one() >> prec//2)
    if T is None:
        T = 2*max(pol.degree() for pol in L)
    S = PowerSeriesRing(C, 'z', T+d)
    basis = [S(str(v)) for v in L.local_basis_expansions(0, T+d)]
    f = V[0].change_ring(C)*vector(basis)
    df = [f]
    for k in range(d):
        f = f.derivatives()
        df.append(f)
    P = hp_approx(df, T)
    try:
        P = [guess_rational(pol) for pol in P]
    except PrecisionError:
        return right_factor(L, prec=2*prec, T=2*T)

    R = OA(P)
    if L%R==0:
        R = OA(R.annihilator_of_composition(z - z0))
        return R
    else:
        return right_factor(L, prec=2*prec, T=2*T)


#Free.<z,Dz> = FreeAlgebra(QQ)
#Dop.<z,Dz> = Free.g_algebra(relations={Dz*z: z*Dz+1})
#dop = (z^2*Dz+3)*((z-3)*Dz+4*z^5)