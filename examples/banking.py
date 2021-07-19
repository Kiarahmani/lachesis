from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
from utils import *
from dsl import *


## EXAMPLE #1 (simple bank account example with a single object)
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
    initial_balance = object_map['balance'][global_counter]
    final_balance = object_map['balance'][global_counter + 1]
    if operation_id == 0:
        return sym_read(initial_balance, final_balance, transaction.vars['x'])
    elif operation_id == 1:
        return Ite(GE(transaction.vars['x'], transaction.args['amount']),
                   sym_dec(initial_balance, final_balance, transaction.args['amount']),
                   do_skip(global_counter, object_map))
    else:
        raise Exception('withdraw has only two operations. Given operation id: ' + str(operation_id))






## EXAMPLE #2 (update two objects with the same value)
def make_update_backup_transaction(identifier, color):
    txn = Transaction('Update', identifier)
    txn.args['value'] = Symbol('wd' + str(txn.identifier) + '_value', INT)
    txn.operation_names.append(tab(2) + 'WRITE(X, new_value)')
    txn.operation_names.append(tab(2) + 'WRITE(Y, new_value)' + '\n}')

    txn.color = color
    txn.constraints = And(GT(txn.args['value'], Int(0)))
    return txn
def update_backup(transaction, operation_id, object_map, global_counter):
    if operation_id == 0:
        return do_write(global_counter, object_map, 'X', transaction.args['value'])
    elif operation_id == 1:
        return do_write(global_counter, object_map, 'Y', transaction.args['value'])
    else:
        raise Exception('trasnaction has only two operations. Given operation id: ' + str(operation_id))


## EXAMPLE #3 (swap values of two objects)
def make_swap_transaction(identifier, color):
    txn = Transaction('Swap', identifier)
    txn.vars['v1'] = Symbol('sw' + str(txn.identifier) + '_v1', INT)
    txn.vars['v2'] = Symbol('sw' + str(txn.identifier) + '_v2', INT)

    txn.operation_names.append(tab(2) + 'LET v1:=READ(X) IN {')
    txn.operation_names.append(tab(4) + 'LET v2:=READ(Y) IN {')

    txn.operation_names.append(tab(6) + 'WRITE(X,v2)')
    txn.operation_names.append(tab(6) + 'WRITE(Y,v1)' + '\n' + tab(4) + "}" + '\n' + tab(2) + "}" + '\n' + '}')

    txn.color = color
    return txn
def swap(transaction, operation_id, object_map, global_counter):
    if operation_id == 0:
        return do_read(global_counter,object_map,'X', transaction.vars['v1'])
    elif operation_id == 1:
        return do_read(global_counter,object_map,'Y', transaction.vars['v2'])
    elif operation_id == 2:
        return do_write(global_counter,object_map,'X', transaction.vars['v2'])
    elif operation_id == 3:
        return do_write(global_counter,object_map,'Y', transaction.vars['v1'])
    else:
        raise Exception('withdraw has only four operations. Given operation id: ' + str(operation_id))


