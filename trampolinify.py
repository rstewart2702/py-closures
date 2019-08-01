def trampolinify(f):
    print("Trampolinization taking place!")
    print("Trampolinizing ", f.__name__)
    def innerTrampoline():
        # r = fi()
        r = f()
        while(callable(r)):
            r = r()
        return r
    #
    return innerTrampoline

def ftt(p1,p2):
    pi1,pi2=p1,p2
    def fti(p1,p2):
        nonlocal pi1,pi2
        if (pi2==4):
            return p1,p2
        pi1,pi2=p1+1,p2+2
        return fi
    def fi():
        return fti(pi1,pi2)
    return fi

@trampolinify
def fmaker(p1,p2):
    def fmakeri():
        return ftt(p1,p2)
    return fmakeri

@trampolinify
def fmaker2():
    return ftt

"""
Decorators are:
+ parse-time transformations:
  + the trampoline-function is executed at program-parse-time:
    It's handed the function defined by the "def" which follows the
    decorator.
    It emits a function-body/lambda that is bound to the name in the
    following "def."
    
  + it results in a function which is designed to accept/receive
    another function/lambda?
  + it receives a 

"""
