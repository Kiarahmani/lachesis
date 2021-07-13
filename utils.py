from pysmt.oracles import get_logic
from pysmt.shortcuts import *
from pysmt.typing import INT
import yaml


# load the configuration file
with open("config.yaml", 'rb') as config_file:
    config = yaml.safe_load(config_file)

# used for printing i number of tabs in the console output
def tab(i):
    return ' '*i

# returns a colored version of the input text
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

# get the input color as string
def known_colored(color, text):
    if color == 'red':
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(255, 110, 110, text)
    elif color == 'blue':
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(160, 160, 255, text)
    elif color == 'green':
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(70, 255, 70, text)
    else:
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(255, 255, 255, text)


# returns an array of symbolic objects (used to model the symbolic state of an object during its life time)
def get_object_array(label, snapshot_cnt, tp):
    return [Symbol(label + "_" + str(i), tp) for i in range(snapshot_cnt)]



# fills the default config args
def get_default_model(query):
    return get_model(query, solver_name=config['solver'], logic='QF_LIA')
