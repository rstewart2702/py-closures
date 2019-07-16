# A sort of tail-call "simulation" via a "trampolined" process?
# The while loop repeatedly invokes the closure, named ftrc,
# which is referenced by variable rv.
# 
def ft(p1,p2):
    pi1=p1; pi2=p2
    #
    def fti(p1,p2):
        nonlocal pi1, pi2
        print(pi1,pi2)
        if (p2==4):
            return None
        pi1=p1+1; pi2=p2+2
        return ftrc
        # fti(p1+1,p2+2)
    #
    def ftrc():
        return fti(pi1,pi2)
    #
    rv=ftrc
    while(rv is not None):
        rv=rv()
    return pi1, pi2

def ftt(p1,p2):
    """
This is a function designed to be trampoline-able.
Returns a reference to a closure designed to be given
to the trampoline() function.
"""
    pi1,pi2 = p1,p2
    def fti(p1,p2):
        nonlocal pi1,pi2
        if(p2==4):
            return p1,p2
        pi1,pi2=p1+1,p2+2
        return ftrc
    #
    def ftrc():
        return fti(pi1,pi2)
    #
    # Return a reference to a closure which invokes
    # the function-which-would-have-used-tail-recursion.
    return ftrc

def trampoline(f):
    """
This is designed to be applied to a trampoline-able function.
"""
    rv = f()
    while(callable(rv)):
        rv=rv()
    return rv
# So, an example of invoking the above would be:
#   trampoline(ftt(0,-1982))
# which returns:
#   (994, 4)
# whereas the recursive version,
#   ftcr(0,-1982)
# would blow up Python's call stack...


##    def ftc(p1p,p2p):
##        pi1=p1+1; pi2=p2+2
##        return fti(pi1,pi2)

def ftr(p1,p2):
    if (p2 == 4):
        return (p1,p2)
    ftr(p1+1,p2+2)


def ft1(p1,p2):
    if (p2==4):
        return None
    return {'p1': p1+1,'p2': p2+2}

def ft1r(p1,p2):
    #
    rval = ft1(p1,p2)
    while (rval is not None):
        lrval = rval
        rval = ft1(rval['p1'],rval['p2'])
    return lrval

# tail recursion would look like:
def ftcr(p1,p2):
    if (p2 == 4):
        return (p1,p2)
    return ftcr(p1+1,p2+2)



"""
What we're really trying to do, however, is come up with a general
way to handle a closure and use it to enclose some state so that it's
wrapped up there and available between invocations?
"""
