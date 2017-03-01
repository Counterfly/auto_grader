from dependencies.cspbase import *
import itertools
import traceback
from utils.utilities import sortInnerMostLists, TO_exc, setTO
from dependencies.test_sudoku_solution import check_solution

import dependencies.solutions.propagators as soln_propagators
import dependencies.solutions.sudoku_csp as soln_model

from utils.test_tools import max_grade

from .test_cases_helpers import *

PROPAGATORS = 'propagators.py'
SUDOKUCSP = 'sudoku_csp.py'

@max_grade(6)
##Tests FC after the first queen is placed in position 1.
def test_simple_FC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = 1200
    did_fail = False

    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)

        setTO(timeout)
        stu_propagators.prop_FC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "FAILED test_simple_FC\nExplanation:\nFC variable domains should be: %r\nFC variable domains are: %r" % (answer,var_domain)
                did_fail = True
                break
        if not did_fail:
            details = "PASS"
            score = 6

    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.print_exc()

    return score, details

@max_grade(6)
##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    did_fail = False
    timeout = 1200

    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        setTO(timeout)
        stu_propagators.prop_GAC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "FAILED test_simple_GAC\nExplanation:\nGAC variable domains should be: %r\nGAC variable domains are: %r" % (answer,var_domain)
                did_fail = True
                break
        if not did_fail:
            details = "PASS"
            score = 6
    except TO_exc:
        details = "got TIMEOUT"

    except:
        details = "Error occurred: %r" % traceback.print_exc()

    return score, details

@max_grade(9)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking GAC.
def three_queen_GAC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = 1200

    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)

        setTO(timeout)
        stu_propagators.prop_GAC(queens)

        answer = [[4],[6, 7, 8],[1],[3, 8],[6, 7],[2, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        if var_vals != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals)

        else:
            details = "PASS"
            score = 9
    except TO_exc:
        details = "got TIMEOUT"
    except Exception:
        details = "Error occurred: %r" % traceback.print_exc()

    return score, details

@max_grade(9)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking FC.
def three_queen_FC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = 1200
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)

        setTO(timeout)
        stu_propagators.prop_FC(queens)

        answer = [[4],[6, 7, 8],[1],[3, 6, 8],[6, 7],[2, 6, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        if var_vals != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals)

        else:
            details = "PASS"
            score = 9
    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.print_exc()

    return score, details
