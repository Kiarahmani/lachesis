# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
#
from utils import *
from dsl import *
from pysmt.shortcuts import *
from pysmt.typing import INT
from pysmt.oracles import get_logic

_SOLVER = 'z3'


def execution_coverage():
    l_i, l_v, l_f, r_i, r_v, r_f = [Symbol(s, INT) for s in
                                    ['l_i', 'l_v', 'l_f', 'r_i', 'r_v', 'r_f']]

    ser_exec = And(
        Equals(r_f, Minus(r_v, Int(10))),
        Equals(r_f, l_i),
        Equals(l_i, l_v),
        Equals(l_f, Minus(l_v, Int(10))))
    # nser_exec = And(Equals(r_i, ns_r_v),
    #                Equals(ns_l_i, ns_l_v),
    #                Equals(ns_l_i, r_i),
    #                Equals(ns_r_f, Minus(ns_r_v, Int(10))),
    #                Equals(ns_l_f, Minus(ns_l_v, Int(10))))

    model = get_model(ser_exec, solver_name=_SOLVER, logic='QF_LIA')
    print('\n<L>')
    print('i: ' + str(model[l_i]))
    print('v: ' + str(model[l_v]))
    print('f: ' + str(model[l_f]))

    print('\n<R>')
    print('i: ' + str(model[r_i]))
    print('v: ' + str(model[r_v]))
    print('f: ' + str(model[r_f]))


def execution_coverage2():
    t1 = Withdraw(id=1, step_cnt=3)
    t2 = Withdraw(id=2, step_cnt=3)

    ser_exec = And(read(t1.balance[0], t1.balance[1], t1.var),
                   Ite(GE(t1.var, t1.amnt), dec(t1.balance[1], t1.balance[2], t1.amnt),
                       Equals(t1.balance[1], t1.balance[2])),
                   # second transaction
                   Equals(t1.balance[2], t2.balance[0]),
                   read(t2.balance[0], t2.balance[1], t2.var),
                   Ite(GE(t2.var, t2.amnt), dec(t2.balance[1], t2.balance[2], t2.amnt),
                       Equals(t2.balance[1], t2.balance[2])))

    t3 = Withdraw(id=3, step_cnt=3)
    t4 = Withdraw(id=4, step_cnt=3)
    nser_exec = And(read(t3.balance[0], t3.balance[1], t3.var),
                    Equals(t3.balance[1], t4.balance[0]),
                    read(t4.balance[0], t4.balance[1], t4.var),
                    Ite(GE(t3.var, t3.amnt), dec(t4.balance[1], t3.balance[2], t3.amnt),
                        Equals(t4.balance[1], t3.balance[2])),
                    Ite(GE(t4.var, t4.amnt), dec(t3.balance[2], t4.balance[2], t4.amnt),
                        Equals(t3.balance[2], t4.balance[2])),
                    )

    seen_models = TRUE()
    final_query = And(nser_exec, ser_exec, GT(t1.amnt, Int(0)), Equals(t1.balance[0], t3.balance[0]),
                      Equals(t1.amnt, t3.amnt), Equals(t2.amnt, t4.amnt), Not(Equals(t2.balance[2], t4.balance[2])))
    for i in range(1):
        model = get_model(And(seen_models, final_query), solver_name=_SOLVER, logic='QF_LIA')
        if model:
            t1.print_model(model)
            t2.print_model(model)
            t3.print_model(model)
            t4.print_model(model)
            # seen_models = And(seen_models, Not(Equals(t4.balance[2],model[t4.balance[2]])))
        else:
            print('no model exists')
        # print("#" * 70)


if __name__ == '__main__':
    print('-' * 100)
    execution_coverage2()
    print('-' * 100)
    print()
