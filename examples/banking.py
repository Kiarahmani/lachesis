from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
from utils import *
from dsl import *






class DEPR_OLD_Withdraw:
    def print_model(self, model, color='white'):
        print(known_colored(color,
                            '\n\nWithDraw#' + str(self.id) + "(amount:" + str(model[self.amount]) + "){"))
        j = 0
        for i in range(len(self.balance) * 2 - 2):
            if i == 1:
                print(tab(2) + known_colored(color, 'LET v := READ(bal) IN{'))
                continue
            elif i == 3:
                print(tab(4) + known_colored(color, 'IF(v>=amount){ DEC(bal,amount) }'))
                print(tab(2) + known_colored(color, '}'))
            database_state = colored(210, 220, 0,
                                     '..' * 20 + '@' + str(j) + '[bal:' + str(model[self.balance[j]]) + ']')
            print(database_state)
            j += 1
        print(known_colored(color, '}'))

    def __init__(self, identifier, step_cnt):
        self.step_cnt = step_cnt
        self.id = identifier
        self.balance = get_object_array('wd' + str(identifier) + '_bal', step_cnt, INT)
        self.var = Symbol('wd' + str(identifier) + '_var', INT)
        self.amount = Symbol('wd' + str(identifier) + '_amount', INT)
