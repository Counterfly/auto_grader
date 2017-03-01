from dependencies.cspbase import *
import itertools
import traceback
from utils.utilities import sortInnerMostLists, TO_exc, setTO
from dependencies.test_sudoku_solution import check_solution

import dependencies.solutions.propagators as soln_propagators
import dependencies.solutions.sudoku_csp as soln_model

from utils.test_tools import max_grade

from .test_cases_helpers import *

#1200
DEFAULT_TIMEOUT = 20
PROPAGATORS = 'propagators.py'
SUDOKUCSP = 'sudoku_csp.py'


@max_grade(6)
##Tests FC after the first queen is placed in position 1.
def test_simple_FC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = DEFAULT_TIMEOUT
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
        details = "Error occurred: %r" % traceback.format_exc()

    return score, details

@max_grade(6)
##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    did_fail = False
    timeout = DEFAULT_TIMEOUT

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
        details = "Error occurred: %r" % traceback.format_exc()

    return score, details

@max_grade(9)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking GAC.
def three_queen_GAC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = DEFAULT_TIMEOUT

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
        details = "Error occurred: %r" % traceback.format_exc()

    return score, details

@max_grade(9)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking FC.
def three_queen_FC(student_modules):
    stu_propagators = student_modules[PROPAGATORS]
    score = 0
    timeout = DEFAULT_TIMEOUT
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
        details = "Error occurred: %r" % traceback.format_exc()

    return score, details


@max_grade(3)
##Checking that importing a sudoku board into model 1 works as expected.
##Passing this test is a prereq for passing check_model_1_constraints.
def model_1_import(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 0
    timeout = DEFAULT_TIMEOUT

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

        answer = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [6], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        lister = []

        for i in range(9):
            for j in range(9):
                lister.append(var_array[i][j].cur_domain())

        if lister != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
        else:
            details = "PASS"
            score = 3
    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.format_exc()
    return score, details


@max_grade(3)
##Checking that importing a sudoku board into model 2 works as expected.
##Passing this test is a prereq for passing check_model_2_constraints.
def model_2_import(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 0
    timeout = DEFAULT_TIMEOUT

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

        answer = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [6], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        lister = []

        for i in range(9):
            for j in range(9):
                lister.append(var_array[i][j].cur_domain())

        if lister != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
        else:
            details = "PASS"
            score = 3
    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.format_exc()
    return score, details


@max_grade(6)
##Checks that model 1 constraints pass when all different, and fail when not all different
def check_model_1_constraints_enum(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 6
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)

        for cons in csp.get_all_cons():
            all_vars = cons.get_scope()
            taken = []
            domain_list = []
            should_pass = []
            should_fail = []
            for va in all_vars:
                domain_list.append(va.cur_domain())
                if len(va.cur_domain()) == 1:
                    taken.append(va.cur_domain()[0])
            for i in range(len(all_vars)):
                va = all_vars[i]
                domain = domain_list[i]
                if len(domain) == 1:
                    should_pass.append(domain[0])
                    should_fail.append(domain[0])
                else:
                    for i in range(1,10):
                        if i in domain and i in taken:
                            should_fail.append(i)
                            break
                    for i in range(1,10):
                        if i in domain and i not in taken:
                            should_pass.append(i)
                            taken.append(i)
                            break
            if cons.check(should_fail) != cons.check(should_pass):
                if cons.check(should_fail) or not cons.check(should_pass):
                    if cons.check(should_fail):
                        details.append("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
                        details.append("var domains:")
                        for va in all_vars:
                            details.append(str(va.cur_domain()))
                    if not cons.check(should_pass):
                        details.append("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
                        details.append("var domains:")
                        for va in all_vars:
                            details.append(str(va.cur_domain()))
                    return 0, "\n".join(details)

    except TO_exc:
        details = "got TIMEOUT"
    except Exception:
        details = "Error occurred: %r" % traceback.format_exc()
        return 0, details

    return score, "PASS"



@max_grade(6)
##Checks that model 1 constraints are implemented as expected.
##Both model_1_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_1_constraints(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 0
    timeout = DEFAULT_TIMEOUT

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]
        answer = [[1, 2, 6], [1, 2, 4, 6], [8], [7], [2, 3, 4, 6, 9], [2, 3, 6, 9], [2, 4, 6], [5], [2, 3, 4, 6], [2, 5, 6, 7], [3], [2, 4, 5, 7], [2, 4, 6], [1], [2, 6, 8], [2, 4, 6, 7], [9], [2, 4, 6, 7], [2, 6, 7], [2, 4, 6], [2, 4, 7, 9], [5], [2, 3, 4, 6, 9], [2, 3, 6, 8, 9], [1], [3, 4, 7, 8], [2, 3, 4, 6, 7], [4], [1, 2, 8], [3], [1, 2, 9], [2, 5, 9], [7], [2, 5], [6], [2, 5], [9], [7], [2, 5], [2, 3, 4, 6], [2, 3, 4, 5, 6], [2, 3, 5, 6], [2, 4, 5], [1], [8], [1, 2, 5, 6], [1, 2, 6], [1, 2, 5], [8], [2, 4, 5, 6], [2, 5, 6], [3], [4, 7], [9], [1, 2, 3, 7, 8], [1, 2, 8], [6], [2, 3, 9], [2, 3, 5, 7, 9], [4], [5, 7, 9], [3, 7], [1, 3, 5, 7], [1, 3, 7], [9], [1, 4, 7], [3, 6], [8], [3, 5, 6], [4, 5, 6, 7], [2], [1, 3, 4, 5, 6, 7], [2, 3, 7], [5], [2, 4, 7], [2, 3, 6, 9], [2, 3, 6, 7, 9], [1], [8], [3, 4, 7], [3, 4, 6, 7]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        lister = []
        soln_propagators.prop_GAC(csp)
        for i in range(9):
            for j in range(9):
                lister.append(var_array[i][j].cur_domain())

        if lister != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
        else:
            details = "PASS"
            score = 6
    except TO_exc:
        details = "got TIMEOUT"
    except Exception:
        details = "Error occurred: %r" % traceback.format_exc()
    return score, details

@max_grade(6)
##Checks that model 1 constraints pass when all different, and fail when not all different
def check_model_2_constraints_enum(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 6
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)

        for cons in csp.get_all_cons():
            all_vars = cons.get_scope()
            taken = []
            domain_list = []
            should_pass = []
            should_fail = []
            for va in all_vars:
                domain_list.append(va.cur_domain())
                if len(va.cur_domain()) == 1:
                    taken.append(va.cur_domain()[0])
            for i in range(len(all_vars)):
                va = all_vars[i]
                domain = domain_list[i]
                if len(domain) == 1:
                    should_pass.append(domain[0])
                    should_fail.append(domain[0])
                else:
                    for i in range(1,10):
                        if i in domain and i in taken:
                            should_fail.append(i)
                            break
                    for i in range(1,10):
                        if i in domain and i not in taken:
                            should_pass.append(i)
                            taken.append(i)
                            break
            if cons.check(should_fail) or not cons.check(should_pass):
                if cons.check(should_fail):
                    details.append("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
                    details.append("var domains:")
                    for va in all_vars:
                        details.append(str(va.cur_domain()))
                if not cons.check(should_pass):
                    details.append("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
                    details.append("var domains:")
                    for va in all_vars:
                        details.append(str(va.cur_domain()))
                return 0, "\n".join(details)

    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.format_exc()
        return 0, details

    return score, "PASS"

@max_grade(6)
##Checks that model 2 constraints are implemented as expected.
##Both model_2_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_2_constraints(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 0
    timeout = DEFAULT_TIMEOUT

    try:
        board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]
        answer = [[1], [4], [8], [7], [2], [9], [6], [5], [3], [6], [3], [5], [4], [1], [8], [2], [9], [7], [7], [2], [9], [5], [6], [3], [1], [8], [4], [4], [8], [3], [1], [9], [7], [5], [6], [2], [9], [7], [2], [3], [5], [6], [4], [1], [8], [5], [6], [1], [8], [4], [2], [3], [7], [9], [8], [1], [6], [2], [7], [4], [9], [3], [5], [3], [9], [4], [6], [8], [5], [7], [2], [1], [2], [5], [7], [9], [3], [1], [8], [4], [6]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        lister = []
        soln_propagators.prop_GAC(csp)
        for i in range(9):
            for j in range(9):
                lister.append(var_array[i][j].cur_domain())

        if lister != answer:
            details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
        else:
            details = "PASS"
            score = 6
    except TO_exc:
        details = "got TIMEOUT"
    except Exception:
        details = "Error occurred: %r" % traceback.format_exc()
    return score, details

###STARTING TESTS THAT WERE NOT RELEASED TO STUDENTS#####

@max_grade(6)
##Checks that model_1 both imports a full board correctly,
##And includes a satisfying tuple iff it is a satisfying tuple and also is in the variable domain
def check_satisfying_tuples_model_1(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 6
    timeout = DEFAULT_TIMEOUT
    details = []
    failed = False

    try:
        board = [ [1,5,2,4,6,9,3,7,8], [7,8,9,2,1,3,4,5,6], [4,3,6,5,8,7,2,9,1], [6,1,3,8,7,2,5,4,9], [9,7,4,1,5,6,8,2,3], [8,2,5,9,3,4,1,6,7], [5,6,7,3,4,8,9,1,2], [2,4,8,6,9,1,7,3,5], [3,9,1,7,2,5,6,8,4]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)

        ##first check that the var domain is set properly
        for i in range(9):
            for j in range(9):
                my_var = var_array[i][j]
                if len(my_var.cur_domain()) != 1:
                    failed = True
                    details.append("FAILED\nExpected var domain for variable at [%d][%d]: [%d];\nReceived var domain for variable at [%d][%d]: %r" % (i,j,board[i][j],i,j,my_var.cur_domain()))
                else:
                    if my_var.cur_domain()[0] != board[i][j]:
                        failed = True
                        score = 0
                        details.append("FAILED\nExpected var domain for variable at [%d][%d]: [%d];\nReceived var domain for variable at [%d][%d]: %r" % (i,j,board[i][j],i,j,my_var.cur_domain()))

        ##Now that we know the variable domains are correct, just check that for each satisfying tuple, the value in the tuple is in the variable domain
        if not failed:
            for con in csp.get_all_cons():
                all_vars = con.get_scope()
                correct_tuple = tuple([x.cur_domain()[0] for x in all_vars])
                sat_tup = list(con.sat_tuples.keys())
                if len(sat_tup) != 1:
                    details.append("FAILED\nExpected satisfying tuples: %r\nReceived satisfying tuples: %r" % ([correct_tuple],sat_tup))
                    failed = True
                    score = 0
                elif sat_tup[0] != correct_tuple:
                    details.append("FAILED\nExpected satisfying tuples: %r\nReceived satisfying tuples: %r" % ([correct_tuple],sat_tup))
                    failed = True
                    score = 0
        if not failed:
            return score, "PASSED"
        else:
            return 0, "\n".join(details)

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(6)
##Checks that model_2 both imports a full board correctly,
##And includes a satisfying tuple iff it is a satisfying tuple and also is in the variable domain
def check_satisfying_tuples_model_2(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 6
    timeout = DEFAULT_TIMEOUT
    details = []
    failed = False

    try:
        board = [ [1,5,2,4,6,9,3,7,8], [7,8,9,2,1,3,4,5,6], [4,3,6,5,8,7,2,9,1], [6,1,3,8,7,2,5,4,9], [9,7,4,1,5,6,8,2,3], [8,2,5,9,3,4,1,6,7], [5,6,7,3,4,8,9,1,2], [2,4,8,6,9,1,7,3,5], [3,9,1,7,2,5,6,8,4]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)

        ##first check that the var domain is set properly
        for i in range(9):
            for j in range(9):
                my_var = var_array[i][j]
                if len(my_var.cur_domain()) != 1:
                    failed = True
                    details.append("FAILED\nExpected var domain for variable at [%d][%d]: [%d];\nReceived var domain for variable at [%d][%d]: %r" % (i,j,board[i][j],i,j,my_var.cur_domain()))
                else:
                    if my_var.cur_domain()[0] != board[i][j]:
                        failed = True
                        score = 0
                        details.append("FAILED\nExpected var domain for variable at [%d][%d]: [%d];\nReceived var domain for variable at [%d][%d]: %r" % (i,j,board[i][j],i,j,my_var.cur_domain()))

        ##Now that we know the variable domains are correct, just check that for each satisfying tuple, the value in the tuple is in the variable domain
        if not failed:
            for con in csp.get_all_cons():
                all_vars = con.get_scope()
                correct_tuple = tuple([x.cur_domain()[0] for x in all_vars])
                sat_tup = list(con.sat_tuples.keys())
                if len(sat_tup) != 1:
                    details.append("FAILED\nExpected satisfying tuples: %r\nReceived satisfying tuples: %r" % ([correct_tuple],sat_tup))
                    failed = True
                    score = 0
                elif sat_tup[0] != correct_tuple:
                    details.append("FAILED\nExpected satisfying tuples: %r\nReceived satisfying tuples: %r" % ([correct_tuple],sat_tup))
                    failed = True
                    score = 0
        if not failed:
            return score, "PASSED"
        else:
            return 0, "\n".join(details)

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(6)
def test_gac_10queens(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 6
    timeout = DEFAULT_TIMEOUT
    did_fail = False

    try:
        queens = nQueens(10)
        curr_vars = queens.get_all_vars()
        curr_vars[3].assign(8)

        sol_queens = nQueens(10)
        sol_vars = sol_queens.get_all_vars()
        sol_vars[3].assign(8)
        soln_propagators.prop_GAC(sol_queens,newVar=sol_vars[3])

        setTO(timeout)
        val, prunes = stu_prop.prop_GAC(queens,newVar=curr_vars[3])
        if not val:
            return 0, "FAILED\nNot a DWO. Expected prop_GAC to return True, prunings. prop_GAC returned False"
        else:
            for i in range(len(curr_vars)):
                if set(curr_vars[i].cur_domain()) != set(sol_vars[i].cur_domain()):
                    curr_vars[i].cur_domain().sort()
                    sol_vars[i].cur_domain().sort()
                    return 0, "FAILED\nExpected output: %r\nOutput received: %r" % (curr_vars[i].cur_domain(),sol_vars[i].cur_domain())
        return score, "PASSED"
    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.format_exc()
    return 0, details

@max_grade(6)
def test_fc_10queens(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    score = 6
    timeout = DEFAULT_TIMEOUT
    did_fail = False

    try:
        queens = nQueens(10)
        curr_vars = queens.get_all_vars()
        curr_vars[3].assign(8)

        sol_queens = nQueens(10)
        sol_vars = sol_queens.get_all_vars()
        sol_vars[3].assign(8)
        soln_propagators.prop_FC(sol_queens,newVar=sol_vars[3])

        setTO(timeout)
        val, prunes = stu_prop.prop_FC(queens,newVar=curr_vars[3])
        if not val:
            return 0, "FAILED\nNot a DWO. Expected prop_FC to return True, prunings. prop_FC returned False"
        else:
            for i in range(len(curr_vars)):
                if set(curr_vars[i].cur_domain()) != set(sol_vars[i].cur_domain()):
                    curr_vars[i].cur_domain().sort()
                    sol_vars[i].cur_domain().sort()
                    return 0, "FAILED\nExpected output: %r\nOutput received: %r" % (curr_vars[i].cur_domain(),sol_vars[i].cur_domain())
        return score, "PASSED"
    except TO_exc:
        details = "got TIMEOUT"
    except:
        details = "Error occurred: %r" % traceback.format_exc()
    return 0, details

@max_grade(12)
def test_DWO(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    score = 12
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    queens = nQueens(6)
    cur_var = queens.get_all_vars()
    cur_var[0].assign(1)
    stu_prop.prop_GAC(queens,newVar=cur_var[0])
    cur_var[1].assign(3)
    pruned = stu_prop.prop_GAC(queens,newVar=cur_var[1])
    answer =  [[1], [3], [6], [], [2], [5]]
    if pruned[0]:
        return 0, "FAILED\nShould result in a DWO.\nExpected variable domains: %r\nVariable domains received: %r" % (answer, [x.cur_domain() for x in cur_var])
    else:
        return score, "PASSED"


##Starting with the bt_search problems

@max_grade(2)
def test_unsolvable_board_model_1(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]

    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_model_unsolvable_board_model_1(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(soln_propagators.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_prop_unsolvable_board_model_1(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = soln_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_unsolvable_board_model_2(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_model_unsolvable_board_model_2(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(soln_propagators.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_prop_unsolvable_board_model_2(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [[0,1,8,0,2,0,0,0,4], [5,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,3],[9,0,1,0,0,5,0,0,0],[0,0,0,0,4,0,0,7,0],[2,0,6,0,0,0,3,0,0],[0,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,4,7,0,0,6,0,0,8]]

        setTO(timeout)
        csp, var_array = soln_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        for i in range(9):
            for j in range(9):
                if var_array[i][j].get_assigned_value() is not None:
                    details.append("FAILED\n[%d][%d] assigned %r; should be assigned None" % (i,j,var_array[i][j].get_assigned_value()))
                    score = 0
                    failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_board1_model_1(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,0,0,0,9,0,0], [0,0,0,0,0,5,0,0,2], [0,7,4,0,1,9,0,6,0], [0,0,2,8,0,0,0,0,0], [8,9,0,0,0,0,0,3,1], [0,0,0,0,0,2,7,0,0],[0,2,0,7,5,0,6,9,0],[4,0,0,1,0,0,0,0,0],[0,0,8,0,0,0,4,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        if not check_solution(var_array):
            score = 0
            details.append("FAILED\nNot a valid sudoku solution")
            failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_model_board1_model_1(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,0,0,0,9,0,0], [0,0,0,0,0,5,0,0,2], [0,7,4,0,1,9,0,6,0], [0,0,2,8,0,0,0,0,0], [8,9,0,0,0,0,0,3,1], [0,0,0,0,0,2,7,0,0],[0,2,0,7,5,0,6,9,0],[4,0,0,1,0,0,0,0,0],[0,0,8,0,0,0,4,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(soln_propagators.prop_GAC)
        details = []
        if not check_solution(var_array):
            details.append("FAILED\nNot a valid sudoku solution")
            score = 0
            failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_prop_board1_model_1(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,0,0,0,9,0,0], [0,0,0,0,0,5,0,0,2], [0,7,4,0,1,9,0,6,0], [0,0,2,8,0,0,0,0,0], [8,9,0,0,0,0,0,3,1], [0,0,0,0,0,2,7,0,0],[0,2,0,7,5,0,6,9,0],[4,0,0,1,0,0,0,0,0],[0,0,8,0,0,0,4,0,0]]

        setTO(timeout)
        csp, var_array = soln_model.sudoku_csp_model_1(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        if not check_solution(var_array):
            details.append("FAILED\nNot a valid sudoku solution")
            failed = True
            score = 0
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_board2_model_2(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,9,0,0,0,0,6], [0,0,7,3,2,4,8,0,1],[8,0,0,0,0,0,0,0,9],[5,7,0,0,9,2,0,0,0],[0,0,0,6,0,1,0,0,0],[0,0,0,5,3,0,0,9,8],[3,0,0,0,0,0,0,0,5],[7,0,5,2,1,3,9,0,0],[2,0,0,0,0,8,6,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        if not check_solution(var_array):
            score = 0
            details.append("FAILED\nNot a valid sudoku solution")
            failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_model_board2_model_2(student_modules):
    stu_model = student_modules[SUDOKUCSP]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,9,0,0,0,0,6], [0,0,7,3,2,4,8,0,1],[8,0,0,0,0,0,0,0,9],[5,7,0,0,9,2,0,0,0],[0,0,0,6,0,1,0,0,0],[0,0,0,5,3,0,0,9,8],[3,0,0,0,0,0,0,0,5],[7,0,5,2,1,3,9,0,0],[2,0,0,0,0,8,6,0,0]]

        setTO(timeout)
        csp, var_array = stu_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(soln_propagators.prop_GAC)
        details = []
        if not check_solution(var_array):
            score = 0
            details.append("FAILED\nNot a valid sudoku solution")
            failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

@max_grade(2)
def test_prop_board2_model_2(student_modules):
    stu_prop = student_modules[PROPAGATORS]
    score = 2
    failed = False
    timeout = DEFAULT_TIMEOUT
    details = []

    try:
        board = [ [0,0,3,9,0,0,0,0,6], [0,0,7,3,2,4,8,0,1],[8,0,0,0,0,0,0,0,9],[5,7,0,0,9,2,0,0,0],[0,0,0,6,0,1,0,0,0],[0,0,0,5,3,0,0,9,8],[3,0,0,0,0,0,0,0,5],[7,0,5,2,1,3,9,0,0],[2,0,0,0,0,8,6,0,0]]

        setTO(timeout)
        csp, var_array = soln_model.sudoku_csp_model_2(board)
        solver = BT(csp)
        solver.bt_search(stu_prop.prop_GAC)
        details = []
        if not check_solution(var_array):
            score = 0
            details.append("FAILED\nNot a valid sudoku solution")
            failed = True
        if not failed:
            details.append("PASSED")

    except TO_exc:
        score = 0
        details.append("got TIMEOUT")
    except:
        score = 0
        details.append("Error occurred: %r" % traceback.format_exc())
    return score, "\n".join(details)

'''
def main(stu_propagators=None, stu_model=None):
    TOTAL_POINTS = 120
    total_score = 0

    import propagators as propagators_soln

    if stu_propagators == None:
        import propagators as stu_propagators
    else:
        import stu_propagators
    if stu_model ==None:
        import sudoku_csp as stu_model
    else:
        import stu_model


    print("---starting test_simple_FC---")
    score, details = test_simple_FC(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_simple_FC---\n")

    print("---starting test_simple_GAC---")
    score, details = test_simple_GAC(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_simple_GAC---\n")

    print("---starting three_queen_FC---")
    score, details = three_queen_FC(stu_propagators)
    print(details)
    total_score += score
    print("---finished three_queen_FC---\n")

    print("---starting three_queen_GAC---")
    score, details = three_queen_GAC(stu_propagators)
    print(details)
    total_score += score
    print("---finished three_queen_GAC---\n")

    print("---starting model_1_import---")
    score, details = model_1_import(stu_model)
    print(details)
    total_score += score
    print("---finished model_1_import---\n")

    print("---starting model_2_import---")
    score, details = model_2_import(stu_model)
    print(details)
    total_score += score
    print("---finished model_2_import---\n")

    print("---starting check_model_1_constraints---")
    score, details = check_model_1_constraints(stu_model)
    print(details)
    total_score += score
    print("---finished check_model_1_constraints---\n")


    print("---starting check_model_2_constraints---")
    score, details = check_model_2_constraints(stu_model)
    print(details)
    total_score += score
    print("---finished check_model_2_constraints---\n")

    print("---starting check_model_1_constraints_enum---")
    score, details = check_model_1_constraints_enum(stu_model)
    print(details)
    total_score += score
    print("---finished check_model_1_constraints_enum---\n")


    print("---starting check_model_2_constraints_enum---")
    score, details = check_model_2_constraints_enum(stu_model)
    print(details)
    total_score += score
    print("---finished check_model_2_constraints_enum---\n")

    print("----------------Starting New test Cases---------------\n")

    print("---starting test_DWO---")
    score, details = test_DWO(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_DWO---")

    print("---starting check_satisfying_tuples_model_1---")
    score, details = check_satisfying_tuples_model_1(stu_model)
    print(details)
    total_score += score
    print("---finished check_satisfying_tuples_model_1---\n")

    print("---starting check_satisfying_tuples_model_2---")
    score, details = check_satisfying_tuples_model_2(stu_model)
    print(details)
    total_score += score
    print("---finished check_satisfying_tuples_model_2---\n")

    print("---starting test_fc_10queens---")
    score, details = test_fc_10queens(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_fc_10queens---\n")

    print("---starting test_gac_10queens---")
    score, details = test_gac_10queens(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_gac_10queens---\n")

    print("---starting test_unsolvable_board_model_1---")
    score, details = test_unsolvable_board_model_1(stu_model,stu_propagators)
    print(details)
    total_score += score
    print("---finished test_unsolvable_board_model_1---\n")

    print("---starting test_prop_unsolvable_board_model_1---")
    score, details = test_prop_unsolvable_board_model_1(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_prop_unsolvable_board_model_1---\n")

    print("---starting test_model_unsolvable_board_model_1---")
    score, details = test_model_unsolvable_board_model_1(stu_model)
    print(details)
    total_score += score
    print("---finished test_model_unsolvable_board_model_1---\n")

    print("---starting test_unsolvable_board_model_2---")
    score, details = test_unsolvable_board_model_1(stu_model,stu_propagators)
    print(details)
    total_score += score
    print("---finished test_unsolvable_board_model_2---\n")

    print("---starting test_prop_unsolvable_board_model_2---")
    score, details = test_prop_unsolvable_board_model_1(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_prop_unsolvable_board_model_2---\n")

    print("---starting test_model_unsolvable_board_model_2---")
    score, details = test_model_unsolvable_board_model_2(stu_model)
    print(details)
    total_score += score
    print("---finished test_model_unsolvable_board_model_2---\n")

    print("---starting test_board1_model_1---")
    score, details = test_board1_model_1(stu_model,stu_propagators)
    print(details)
    total_score += score
    print("---finished test_board1_model_1---\n")

    print("---starting test_model_board1_model_1---")
    score, details = test_model_board1_model_1(stu_model)
    print(details)
    total_score += score
    print("---finished test_model_board1_model_1---\n")

    print("---starting test_prop_board1_model_1---")
    score, details = test_prop_board1_model_1(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_prop_board1_model_1---\n")

    print("---starting test_board2_model_2---")
    score, details = test_board2_model_2(stu_model,stu_propagators)
    print(details)
    total_score += score
    print("---finished test_board2_model_2---\n")

    print("---starting test_model_board2_model_2---")
    score, details = test_model_board2_model_2(stu_model)
    print(details)
    total_score += score
    print("---finished test_model_board2_model_2---\n")

    print("---starting test_prop_board2_model_2---")
    score, details = test_prop_board2_model_2(stu_propagators)
    print(details)
    total_score += score
    print("---finished test_prop_board2_model_2---\n")


    if total_score == TOTAL_POINTS:
        print("Score: %d/%d; Passed all tests; Will pass assignment with >= 50pct mark" % (total_score,TOTAL_POINTS))
    else:
        print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))


if __name__=="__main__":
    main()
'''
