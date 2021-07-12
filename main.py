import yaml
from utils import *
from dsl import *
from pysmt.shortcuts import *
from pysmt.typing import INT
from pysmt.oracles import get_logic
from examples.banking import *

# load the configuration file
with open("config.yaml", 'rb') as config_file:
    config = yaml.safe_load(config_file)


class Execution(object):
    object_map = {}
    constraints = None

    def __init__(self, identifier, object_names, transactions, orders):
        self.identifier = identifier
        self.length = len(orders) + 1
        self.orders = orders
        self.transactions = transactions
        for name in object_names:
            self.object_map[name] = get_object_array(name, self.length, INT)

    def print_execution(self, model):
        # initialize the transaction pointers
        transaction_pointer = {}
        for i in range(len(self.transactions)):
            transaction_pointer[i] = 0

        # iterate over all steps in the execution and print the database state + the executed operations
        for i in range(self.length):
            # print the value of all objects
            for key in self.object_map.keys():
                object_name = self.object_map[key]

                database_state = colored(150, 150, 150, "--" * 15 +
                                         " " + key + " = " + str(model[object_name[i]]))
                print(database_state)

            if i == self.length - 1:
                break
            # print the next operation from the next transaction
            next_transaction = self.transactions[self.orders[i]]
            transaction_header = known_colored(next_transaction.color,
                                               next_transaction.name +
                                               "(" + ','.join(
                                                   arg + ":" + str(model[next_transaction.args[arg]]) for arg in
                                                   next_transaction.args) + "){")

            transaction_body = known_colored(next_transaction.color,
                                             next_transaction.operation_names[transaction_pointer[self.orders[i]]])
            # print the header only before the first operation
            if transaction_pointer[self.orders[i]] == 0:
                print(transaction_header + '\n' + transaction_body)
            else:
                print(transaction_body)
            # update the pointer
            transaction_pointer[self.orders[i]] += 1


class Transaction(object):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
        self.args = {}
        self.vars = {}
        self.operation_names = []
        self.color = 'white'


def make_withdraw_transaction(identifier):
    txn = Transaction('Withdraw', identifier)
    txn.args['amount'] = Symbol('wd' + str(txn.identifier) + '_amount', INT)
    txn.vars['x'] = Symbol('wd' + str(txn.identifier) + '_x', INT)
    txn.operation_names.append(tab(2) + 'LET x:=READ(balance) IN {')
    txn.operation_names.append(tab(4) + 'IF(x>amount){ \n' +
                               tab(6) + 'DEC(balance, amount)\n' +
                               tab(4) + '}\n' +
                               tab(2) + '}\n' + '}')
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


def make_execution(identifier, transactions, object_names, orders):
    # initialize an execution
    execution = Execution(identifier, object_names, transactions, orders)
    # initialize the program counter to 0 for all transactions
    transaction_counter = {}
    global_counter = 0
    for order in orders:
        transaction_counter[order] = 0

    # construct the symbolic constraints of the execution
    all_execution_constraints = TRUE()
    for order in orders:
        # constrain the values of objects, based on the next transaction to be executed
        current_transaction = transactions[order]
        current_transaction_counter = transaction_counter[order]
        new_constraints = make_withdraw_constraints(current_transaction, current_transaction_counter,
                                                    execution.object_map, global_counter)
        all_execution_constraints = And(all_execution_constraints, new_constraints)
        # update the local and the global counters
        transaction_counter[order] += 1
        global_counter += 1
    execution.constraints = all_execution_constraints
    return execution


def run_analysis():
    t1 = make_withdraw_transaction(1)
    t1.color = 'blue'
    t2 = make_withdraw_transaction(2)
    t2.color = 'red'
    e1 = make_execution(identifier=1, transactions=[t1, t2], object_names=['balance'], orders=[0, 0, 1, 1])
    #e2 = make_execution(identifier=1, transactions=[t1, t2], object_names=['balance'], orders=[0, 1, 0, 1])

    final_query = And(e1.constraints,
                      #e2.constraints,
                      # enforce a particular program path
                      LT(t1.args['amount'], e1.object_map['balance'][0]),
                      #LT(t1.args['amount'], e2.object_map['balance'][0]),
                      # enforce positive amounts to be withdrawn
                      GT(t1.args['amount'], Int(0)),
                      GT(t2.args['amount'], Int(0))
                      )

    model = get_model(final_query, solver_name=config['solver'], logic='QF_LIA')
    if model:
        e1.print_execution(model)
        #print('\n\n')
        #e2.print_execution(model)
    else:
        print('model does not exist')
    return


if __name__ == '__main__':
    run_analysis()
