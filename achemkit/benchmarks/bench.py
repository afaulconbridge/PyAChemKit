import time

import AChemKit


def benchmark(func, *args, **kwargs):
    """
    Runs supplied function with supplied arguments.
    Prints to std out the name of function and time elapsed.
    """
    starttime = time.clock()
    func(*args, **kwargs)
    endtime = time.clock()
    print func.__name__, "%7.3fsec"%(endtime-starttim)
    

if __name__ == "__main__":
    pass
