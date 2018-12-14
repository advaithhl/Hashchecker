from colorama import Style as st
from colorama import Back as bgc


def blue(string):
    return bgc.BLUE + string + bgc.RESET


def green(string):
    return bgc.GREEN + string + bgc.RESET


def red(string):
    return bgc.RED + string + bgc.RESET


def dim(string):
    return st.DIM + string + st.RESET_ALL
