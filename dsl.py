from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
from utils import *


def read(init, final, variable):
    return And(Equals(init, final), Equals(variable, init))


def write(init, final, value):
    return And(Equals(final, value))


def dec(init, final, value):
    return And(Equals(final, Minus(init, value)))


def get_object_array(label, snapshot_cnt, tp):
    return [Symbol(label + "_" + str(i), tp) for i in range(snapshot_cnt)]


class Withdraw:
    def print_model(self, model):
        print('\n\nWithDraw#' + str(self.id) + "(amnt:" + str(model[self.amnt]) + "){")
        j = 0
        for i in range(len(self.balance) * 2 - 2):
            if i == 1:
                print(tab(2) + 'LET v := READ(bal) IN{')
                continue
            elif i == 3:
                print(tab(4) + 'IF(v>=amnt){ DEC(bal,amnt) }')
                print(tab(2) + '}')
            print('. ' * 20 + 'model@' + str(j) + '[bal:' + str(model[self.balance[j]]) + ']')

            j += 1

    def __init__(self, id, step_cnt):
        self.step_cnt = step_cnt
        self.id = id
        self.balance = get_object_array('wd' + str(id) + '_bal', step_cnt, INT)
        self.var = Symbol('wd' + str(id) + '_var', INT)
        self.amnt = Symbol('wd' + str(id) + '_amnt', INT)
