from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
from utils import *
from dsl import *


def make_withdraw_transaction(identifier, color):
    txn = Transaction('Withdraw', identifier)
    txn.args['amount'] = Symbol('wd' + str(txn.identifier) + '_amount', INT)
    txn.vars['x'] = Symbol('wd' + str(txn.identifier) + '_x', INT)
    txn.operation_names.append(tab(2) + 'LET x:=READ(balance) IN {')
    txn.operation_names.append(tab(4) + 'IF(x>amount){ \n' +
                               tab(6) + 'DEC(balance, amount)\n' +
                               tab(4) + '}\n' +
                               tab(2) + '}\n' + '}')
    txn.color = color
    txn.constraints = And(GT(txn.args['amount'], Int(0)))
    return txn


def make_withdraw_constraints(transaction, operation_id, object_map, global_counter):
    initial_object = object_map['balance'][global_counter]
    final_object = object_map['balance'][global_counter + 1]
    if operation_id == 0:
        return sym_read(initial_object, final_object, transaction.vars['x'])
    elif operation_id == 1:
        return Ite(GE(transaction.vars['x'], transaction.args['amount']),
                   sym_dec(initial_object, final_object, transaction.args['amount']),
                   Equals(initial_object, final_object))
    else:
        raise Exception('withdraw has only two operations. Given operation id: ' + str(operation_id))
