#Utilities
import signal

def containsList(lst):
    '''true if lst contains lists'''
    if not isinstance(lst, list):
        return False
    for e in lst:
        if isinstance(e, list):
            return True
    return False
    
def sortInnerMostLists(lst):
    '''sort the innermost lists in a list of lists of lists...'''
    if not isinstance(lst, list):
        return
    elif containsList(lst):
        for e in lst:
            sortInnerMostLists(e)
    else:
        lst.sort()

class TO_exc(Exception):
    pass

def toHandler(signum, frame):
    raise TO_exc()

def setTO(TOsec):
    signal.signal(signal.SIGALRM, toHandler)
    signal.alarm(TOsec)
