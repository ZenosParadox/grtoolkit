import math, numpy as np
from sympy import sympify, solve, solve_poly_system, symbols
from re import sub
import grtoolkit.Math.sympyInterface
from grtoolkit.Math.sympyInterface import preSympifySub

def magnitude(*args):
    '''Square root of sum'''
    square_sum = 0
    for arg in args:
        square_sum += arg**2
    return math.sqrt(square_sum)

def roundSig(x, sig=5):
    '''Round numbers to specified significant figures'''
    if x == 0:
        return 0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def delta(p1,p2):
    '''Returns absolute difference between two numbers'''
    return abs(p2-p1)

def softmax(L):
    '''
    Function that takes as input a list of numbers, 
    and returns the list of values given by the softmax function.
    
    Example:
    Input [1,2,3]
    Output [e**1/(e**1 + e**2 + e**3),
            e**2/(e**1 + e**2 + e**3)
            e**3/(e**1 + e**2 + e**3)]'''
    return [np.exp(x)/sum(np.exp(L)) for x in L]

def sigmoid(x):
    return 1/(1+np.exp(-x))

def cross_entropy(Y, P):
    '''
    Sample inputs: Y=[1,1,0] and P=[0.8,0.7,0.1] Equal 0.69
    Where,
    Y is list of whether events are on or off
    P is list of probabilities if events are on
    
    Formula is sum of all cases of entropy if event is active plus entropy if event is inactive
    
    Events with high probabilities have low cross entopy
    Events with low proabilities have high cross entropy

    OR

    High cross entropy means low probability
    Low cross entropy means high probability
    '''
   
    Y = np.float_(Y)
    P = np.float_(P)
    return -np.sum(Y * np.log(P) + (1 - Y) * np.log(1 - P))

def algebraSolve(expr, solve_for,**kwargs):
    """
    Solves single algebraic string equation. 
    
    Usage: algebraSolve("x**2 + 3*x - 1/2 + y", "x", y=24)

    Returns: [ans]
    """
    expr = preSympifySub(expr,**kwargs)
    expr=sympify(expr)
    #GENERATE VARIABLE SYMBOLS FROM EXPRESSION
    # if expr.free_symbols: # if expr.freesymbols is not empty
    if not isinstance(expr,bool):
        for sym in expr.free_symbols: 
            exec(f"{sym.name}=symbols('{sym.name}')")
            #MAKE solve_for STRING EQUAL REQUIRED EXPRESSION VARIABLE SYMBOL
            if solve_for == sym.name:    
                solve_for = sym
            # SUBSTITUTE KARGs FOR EXPRESSION SYMBOLS
            for k, v in kwargs.items():
                if k == sym.name:
                    expr=expr.subs(k,v)
        return solve(expr, solve_for)
    else:
        return expr #if expression not possible, just return expression

def solveEqs(eq, find, printEq=True, **kwargs):
    """
    Solves multiple equations independently in search for variable.
    Allows substitution via kwargs.
    In other words, algebraSolve() on multiple equations at once.

    Usage:
        eq = list()
        eq.append("Eq(a_tan, dv/dt)")
        eq.append("Eq(a_tan, r*dw/dt)")
        eq.append("Eq(a_tan, r*alpha)")
        solveEqs(eq, "a_tan", printEq=printEq, **kwargs)

    Returns:
        [
            ans1,
            ans2,
            ans3
        ]
    """
    #CREATE SET OF ARGUMENTS SUPPLIED TO FUNCTION
    original_eq_ref = eq.copy()
    availSet = {find}
    for k,v in kwargs.items():
        availSet.add(k)
        v=str(v)
    eq = [preSympifySub(expr,**kwargs) for expr in eq]
    eq = [sympify(expr) for expr in eq]
    freesym = [expr.free_symbols for expr in eq]
    freevar = []
    solution = list()
    #CONVERT LIST OF SETS OF SYMBOLS INTO LIST OF SETS OF STR
    for freeset in freesym:
        tempset = set()
        for sym in freeset:
            tempset.add(sym.name)
        freevar.append(tempset)
    unknowns = [freeset-availSet for freeset in freevar]            # Eliminate variables requested in function arguments: find and knowns
    unknowns_count = [len(unknownset) for unknownset in unknowns]   # How many unknowns are left in each equation?
    find_avail = [find in freevarset for freevarset in freevar]     # Is the variable in question available in this equation?
    index = list(range(len(unknowns_count)))
    zipper = list(zip(index, unknowns_count, find_avail))

    for zippedList in zipper:
        solution.append(algebraSolve(eq[zippedList[0]],find, **kwargs))

    printEquationsSolution(original_eq_ref, solution, find, printEq=printEq) #print Equations and Solutions to console
    return solution

def printEquations(eq):
    # print("Equations:\n")
    for equation in eq:
        print(equation)

def printEquationsSolution(eq, solution, find, printEq=True):
    print("\n")
    if printEq:
        for i in range(len(eq)):
            print(
f"""
OPTION {i}
From Equation: {eq[i]}:
{find} = {str(solution[i])}"""
)
        # print("Equations"), printEquations(eq), print("\n")
        # print("Solutions"), printEquations(solution), print("\n")

def solveSimultaneousEqs(eq):
    '''
    Solve Simultaneous Equations
    Finite solutions only. No expression based answers.

    Usage:
    eq = list()
    eq.append("-x/10-x/5-6-(x-y)/2")
    eq.append("y/4-3-6-(x-y)/2")
    solveSimultaneousEqs(eq)
    '''

    eq = [sympify(expr) for expr in eq]
    freesym = [expr.free_symbols for expr in eq]
    freevar = list()
    for freeset in freesym:
        for sym in freeset:
            freevar.append(sym)
    freevar=list(set(freevar))
    for sym in freevar:
        exec(f"{sym.name}=symbols('{sym.name}')")

    solutions = solve_poly_system(eq, freevar)
    solutionList = list()

    freevar = [str(var) for var in freevar]

    for possibility in solutions:
        possibility = [float(num) for num in possibility]
        solutionList.append(dict(zip(freevar,possibility)))
        return solutionList

def sourceFreeSeriesEquivalentCircuit(R, C, L, find="i", printEq=True, **kwargs):
    alpha = R / (2 * L)
    w0 = 1 / (L*C)**(1/2)
    s1 = -alpha + (alpha**2 - w0**2)**(1/2)
    s2 = -alpha - (alpha**2 - w0**2)**(1/2)
    # j = (-1)**(1/2)
    # j = complex(1)

    eq = list()
    if alpha > w0:
        eq.append("Eq(i, A1*exp(s1*t) + A2*exp(s2*t))")
    if alpha == w0: #C=4*L/R**2
        eq.append("Eq(i, (A2 + A1*t)*exp(-alpha*t))")
    if alpha < w0:
        # wd = (w0**2 - alpha**2)**(1/2)
        # B1 = A1 + A2
        # B2 = j*(A1 - A2)
        eq.append("Eq(i, exp(-alpha*t)*(B1*cos(wd*t) + B2*sin(wd*t)))")

    kwargs.update({"wd": "(w0**2 - alpha**2)**(1/2)", "alpha": alpha, "w0":w0, "s1":s1, "s2":s2, "B1": "A1 + A2", "B2": "j*(A1 - A2)"})

    return solveEqs(eq,find="i", printEq=printEq, **kwargs)

if __name__ == "__main__":
    sourceFreeSeriesEquivalentCircuit(R=5,C=4*1/5**2,L=1)

    # Eq(i, exp(-(2.5)*t)*((A1 + A2)*cos((((10.0)**2 - (2.5)**2)**(1/2))*t) + (j*(A1 - A2))*sin((((10.0)**2 - (2.5)**2)**(1/2))*t))