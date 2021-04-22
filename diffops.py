from sage.rings.rational_field import QQ
from sage.rings.qqbar import QQbar
from sage.arith.functions import lcm
from ore_algebra import DifferentialOperators
from sage.rings.polynomial.polynomial_ring import PolynomialRing_field



def is_fuchsian(L):

    r"""
    Return True if L is fuchian, False if not.

    Use Fuch's criterion: Let L = a_n*Dz^n + ... + a_0 be an operator whose
    coefficients are polynomial and p be a finite singular point of L. Then p is
    regular iff no (z-p)^{n-k}*a_k/a_n admits p as pole.

    """

    F = L.base_ring()
    z, n = F.gen(), L.order()

    if not isinstance(F, PolynomialRing_field):
        q = lcm([c.denominator() for c in L])
        L = L.parent().change_ring(L.base_ring().base())(q*L)

    sing = L.leading_coefficient().roots(QQbar, multiplicities=False)

    for k, frac in enumerate(L.monic().coefficients()[:-1]):
        for p in sing:
            d = ((z-p)**(n-k)*frac).denominator()
            if d(p)==0:
                return False

    L = L.annihilator_of_composition(1/z)
    for k, frac in enumerate(L.monic().coefficients()[:-1]):
        d = (z**(n-k)*frac).denominator()
        if d(0)==0:
            return False

    return True