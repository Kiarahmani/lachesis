from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
from utils import *
from enum import Enum


# symbolic database operations
# read operation: takes the initial and final symbolic states and returns the logical relationship between them
def sym_read(init, final, variable):
    return And(Equals(init, final), Equals(variable, init))

# write operation: takes the initial and final symbolic states and returns the logical relationship between them
# the initial is not constrained -- is passed as an argument for uniformity between database operations
def sym_write(init, final, value):
    return And(Equals(final, value))

# decrement operation
def sym_dec(init, final, value):
    return And(Equals(final, Minus(init, value)))

# increment operation
def sym_inc(init, final, value):
    return And(Equals(final, Plus(init, value)))



class Execution(object):
    def __init__(self, identifier, object_names, transactions, orders):
        self.identifier = identifier
        self.length = len(orders) + 1
        self.orders = orders
        self.transactions = transactions
        self.object_map = {}
        self.constraints = None
        for name in object_names:
            self.object_map[name] = get_object_array('e' + str(identifier) + '_' + name, self.length, INT)

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
        self.constraints = None










