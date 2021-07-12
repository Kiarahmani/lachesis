from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT


def tab(i):
    return ' '*i
def all_smt(formula, keys):
    target_logic = get_logic(formula)
    print("Target Logic: %s" % target_logic)
    with Solver(logic=target_logic) as solver:
        solver.add_assertion(formula)
        while solver.solve():
            partial_model = [EqualsOrIff(k, solver.get_value(k)) for k in keys]
            print(partial_model)
            solver.add_assertion(Not(And(partial_model)))



# if I is an interpolant for A and B, return true
def check_interpolant(X, Y, I):
    print ('\n')
    b1 = is_sat(And(I,Y))
    b2 = is_valid(Implies(X,I))
    res = (not b1 and b2)
    print ("checking if I is an interpolant for X and Y: " + str(res))
    print (tab(2) + '')


