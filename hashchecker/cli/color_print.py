from colorama import Style as st
from colorama import Back as bgc


def blue(string):
    print(bgc.BLUE + string + bgc.RESET)


def red(string):
    print(bgc.RED + string + bgc.RESET)


def dim(string):
    print(st.DIM + string + st.RESET_ALL)
