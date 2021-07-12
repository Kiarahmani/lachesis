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











