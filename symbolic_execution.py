from dsl import *


# returns an execution instance with constraints initialized to capture the interleaved execution of the given
# transaction instances according to the given interleaved order
def make_execution(identifier, transactions, object_names, orders, transactional_constraints_gen):
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
        new_constraints = transactional_constraints_gen(current_transaction, current_transaction_counter,
                                                        execution.object_map, global_counter)
        all_execution_constraints = And(all_execution_constraints, new_constraints)
        # update the local and the global counters
        transaction_counter[order] += 1
        global_counter += 1
    execution.constraints = all_execution_constraints
    return execution


# asserts that all objects at the beginning of both executions have the same value
def assert_initial_db_eq(e1, e2):
    assert e1.object_map.keys() == e2.object_map.keys()
    res = TRUE()
    for key in e1.object_map.keys():
        res = And(res, Equals(e1.object_map[key][0], e2.object_map[key][0]))
    return res


# asserts that all objects at the end of the execution have different values
def assert_final_db_neq(e1, e2):
    assert e1.object_map.keys() == e2.object_map.keys()
    assert e1.length == e2.length
    last_index = e1.length - 1
    res = TRUE()
    for key in e1.object_map.keys():
        res = And(res, Not(Equals(e1.object_map[key][last_index], e2.object_map[key][last_index])))
    return res


# asserts that arguments to both transactions are equal
def assert_args_eq(t1, t2):
    assert t1.args.keys() == t2.args.keys()
    res = TRUE()
    for arg in t1.args.keys():
        res = And(res, Equals(t1.args[arg], t2.args[arg]))
    return res


# asserts that all objects initially are positive (specific use-cases only)
def assert_positive_init_db(e1):
    res = TRUE()
    for key in e1.object_map.keys():
        res = And(res, (GT(e1.object_map[key][0], Int(0))))
    return res


# asserts that final database state is not equal to the values assigned in the given model
def assert_final_db_distinct(e1, model):
    res = TRUE()
    last_index = e1.length - 1
    for key in e1.object_map.keys():
        res = And(res, Not(Equals(e1.object_map[key][last_index], model[e1.object_map[key][last_index]])))
    return res
