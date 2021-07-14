import yaml
from utils import *
from dsl import *
from pysmt.shortcuts import *
from pysmt.typing import INT
from pysmt.oracles import get_logic
from examples.banking import *
from symbolic_execution import *
import time

# load the configuration file
with open("config.yaml", 'rb') as config_file:
    config = yaml.safe_load(config_file)

# a simple bank account example -- with a single object
def run_analysis():
    t1 = make_withdraw_transaction(1, 'blue')
    t2 = make_withdraw_transaction(2, 'red')
    t3 = make_withdraw_transaction(3, 'blue')
    t4 = make_withdraw_transaction(4, 'red')

    e1 = make_execution(identifier=1, transactions=[t1, t2], object_names=['balance'],
                        orders=[0, 0, 1, 1], transactional_constraints_gen=make_withdraw_constraints)
    e2 = make_execution(identifier=2, transactions=[t3, t4], object_names=['balance'],
                        orders=[0, 1, 0, 1], transactional_constraints_gen=make_withdraw_constraints)

    unified_query = And(e1.constraints, e2.constraints,
                        t1.constraints, t2.constraints, t3.constraints, t4.constraints,
                        # assertions on transaction arguments
                        assert_args_eq(t1, t3), assert_args_eq(t2, t4),
                        # assertions on database states
                        assert_positive_init_db(e1), assert_positive_init_db(e2),
                        assert_initial_db_eq(e1, e2), assert_final_db_neq(e1, e2))

    seen_counter_examples = TRUE()

    for i in range(5):
        unified_model = get_default_model(And(seen_counter_examples, unified_query))
        if unified_model:
            e1.print_execution(unified_model)
            print('\n\n\n\n')
            e2.print_execution(unified_model)
            seen_counter_examples = And(seen_counter_examples,
                                        assert_final_db_distinct(e1,unified_model),
                                        assert_final_db_distinct(e2,unified_model))
        else:
            print('no model exists')
        #print('\n')
        final_index = e1.length - 1
        for obj in e1.object_map.keys():
            o1 = unified_model[e1.object_map[obj][final_index]]
            o2 = unified_model[e2.object_map[obj][final_index]]
            print ('E1=%s  E2=%s      ' % (o1 , o2))
        #print(colored(230, 230, 160, "*" * 100))
        #print('\n')


# introducing multiple objects
def run_analysis2():
    t1 = make_swap_transaction(1, 'blue')
    t2 = make_swap_transaction(2, 'red')
    t3 = make_swap_transaction(3, 'blue')
    t4 = make_swap_transaction(4, 'red')

    e1 = make_execution(identifier=1, transactions=[t1, t2], object_names=['X', 'Y'],
                        orders=[0, 0, 0, 0, 1, 1, 1, 1], transactional_constraints_gen=swap)
    e2 = make_execution(identifier=2, transactions=[t3, t4], object_names=['X', 'Y'],
                        orders=[0, 0, 1, 0, 0, 1, 1, 1], transactional_constraints_gen=swap)

    unified_query = And(e1.constraints, e2.constraints,
                        t1.constraints, t2.constraints, t3.constraints, t4.constraints,
                        # assertions on transaction arguments
                        assert_args_eq(t1, t3), assert_args_eq(t2, t4),
                        # assertions on database states
                        assert_positive_init_db(e1), assert_positive_init_db(e2),
                        assert_initial_db_eq(e1, e2),
                        assert_any_final_db_neq(e1, e2)
                        )

    seen_counter_examples = TRUE()


    for i in range(100):
        print(colored(230, 230, 160, "=" * 35 + ' Run('+str(i+1)+') '+'='*35))
        unified_model = get_default_model(And(seen_counter_examples, unified_query))
        if unified_model:
            if config['_print_transactions_in_executions']:
                e1.print_execution(unified_model)
                print('\n\n\n\n')
                e2.print_execution(unified_model)
            seen_counter_examples = And(seen_counter_examples,
                                        assert_final_db_distinct(e1,unified_model),
                                        assert_final_db_distinct(e2,unified_model))
            final_index = e1.length - 1
            for obj in e1.object_map.keys():
                o1 = unified_model[e1.object_map[obj][final_index]]
                o2 = unified_model[e2.object_map[obj][final_index]]
                o_i = unified_model[e1.object_map[obj][0]]
                print (str(obj) + ': init=%s  ser_f=%s  nser_f=%s      ' % (o_i,o1 , o2))
        else:
            print('no model exists')





if __name__ == '__main__':
    start_time = time.time()
    run_analysis2()
    print("\n\n\n --- execution time: %.4f s ---" % (time.time() - start_time))
