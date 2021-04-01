

def clean_pol(pol):
    l = pol.coefficients()
    while len(l)>0 and l[-1].contains_zero(): l.pop()
    return pol.parent()(l)



def GCD(a, b):

    """
    Return a *non-rigorous* gcd of the polynomials "a" and "b".

    Note: this function is designed for BallField as base ring.

    Some words about the correction of this function:
    Let a· and b· be fixed. If a and b are precise enough, GCD(a, b) contains
    the gcd of a and b.

    INPUT:

     -- "a" -- polynomial
     -- "b" -- polynomial

    OUTPUT:

     -- "a" -- polynomial


    EXAMPLES::
    """

    a, b = clean_pol(a), clean_pol(b)
    if a==0: return b
    if b==0: return a
    if a.degree() < b.degree(): return GCD(b, a)

    while b != 0:
        a, b = b, a.quo_rem(b)[1]
        b = clean_pol(b)

    return a



def XGCD():
    return



def radical(pol):

    r"""
    Return a *non-rigorous* radical of the polynomial "pol".

    Note: this function is designed for BallField as base ring.

    Some words about the correction of this function:
    Let pol· be fixed. If pol is precise enough, radical(pol)) contains the
    radical of pol·.


    INPUT:

     -- "pol" -- polynomial


    OUTPUT:

     -- "rad" -- polynomial


    EXAMPLES::
    """

    d = GCD(pol, pol.derivative())
    rad = clean_pol(pol.quo_rem(d)[0])

    return rad
