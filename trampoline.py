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

"""
So,
we'd like a decorator to take away some of the syntactical pain.

So that:
  @trampoline2
  def ft(p1,p2) ....
would be nice.

What about 

"""

def trampolinized(f):
    # fi = f()
    #
    def innerTrampoline():
        # r = fi()
        r = f()
        while(callable(r)):
            r = r()
        return r
    #
    return innerTrampoline


def ftt1(p1,p2):
    pi1,pi2 = p1,p2
    #
    def fti(p1,p2):
        nonlocal pi1,pi2
        if(p2==4):
            return p1,p2
        pi1,pi2=p1+1,p2+2
        return ftrc
    def ftrc():
        return fti(pi1,pi2)
    return trampolinized(ftrc)


def ftt2(p1,p2):
    pi1,pi2 = p1,p2
    #
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
    # This shows how there is potential to use a decorator in order
    # to "trampoline-ize" this "tail-recursive" process, in a
    # rather general fashion:
    @trampolinized
    def fi():
        return ftrc
    #
    return fi()
    
def ftt3(p1,p2):
    pi1,pi2 = p1,p2
    #
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
    return trampolinized(ftrc)()

def ftt4(p1,p2):
    pi1,pi2 = p1,p2
    #
    def fti(p1,p2):
        nonlocal pi1,pi2
        if(p2==4):
            return p1,p2
        pi1,pi2=p1+1,p2+2
        return ftrc
    #
    @trampolinized
    def ftrc():
        return fti(pi1,pi2)
    #
    return ftrc()




def trampoline2(f):
    fi = f()
    #
    def innerTrampoline():
        r = fi()
        while(callable(r)):
            r = r()
        return r
    #
    return innerTrampoline

##f1 = ftt(0,1982)
##@trampoline
##def fttid():
##    return f1

##@trampoline2
##def ftt1o(p1,p2):
##    return ftt(p1,p2)
##
##@trampoline2
##def ftt1o1(**kwargs):
##    pi1=kwargs['p1']; pi2=kwargs['p2']
##    #
##    def fti(p1,p2):
##        nonlocal pi1, pi2
##        if(p2==4):
##            return p1,p2
##        pi1,pi2=p1+1,p2+2
##        return ftrc
##    #
##    def ftrc():
##        return fti(pi1,pi2)
##    #
##    return ftrc


##@trampoline2(**kwargs)
##def ftt1(**kwargs):
##    return ftt(kwargs['p1'],kwargs['p2'])

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
