"""
Various small functions that can get lumped together into this module.
"""
import math
import random

def get_sample(distribution, rng=None):
    """
    Samples a provided distribution at random.
    
    Distribution can be a single number (int or float), always returns the same value
    
    Distribution can be a sequence (list or tuple) which will be uniformly sampled from
    Duplicates can be used to adjust frequencies.
    
    Distribution can be a mapping (dict) where the keys are things to be returned and
    values are the relative weightings.
    
    """
    if rng is None:
        rng = random.Random()
    if isinstance(distribution, int) or isinstance(distribution, float):
        return distribution
    elif isinstance(distribution, list) or isinstance(distribution, tuple):
        return (rng.sample(distribution, 1))[0]
    elif isinstance(distribution, dict):
        #assume its a value:proportion dict
        total = sum(distribution.values())
        target = rng.random()*total
        i = 0
        score = distribution.values()[i]
        hit = distribution.keys()[i]
        while score < target:
            i += 1
            score += distribution.values()[i]
            hit = distribution.keys()[i]
        return hit

def long_subseq(data):
    """
    Given some sequences --- strings, tuples, lists, etc --- return the 
    longest subsequence common to all sequences.
    """
    substr = ''
    for i in range(len(data[0])):
        for j in range(len(data[0])-i+1):
            if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                substr = data[0][i:i+j]
    return substr
           
def memory_free():
    """Returns the amount of memory free, in megabytes"""
    import os
    if os.name == "posix":
        """Returns the RAM of a linux system"""
        totalMemory = os.popen("free -m").readlines()[1].split()[3]
        return int(totalMemory)   
    elif os.name == "nt":
        """Uses Windows API to check RAM in this OS"""
        import ctypes
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ("dwLength", c_ulong),
                ("dwMemoryLoad", c_ulong),
                ("dwTotalPhys", c_ulong),
                ("dwAvailPhys", c_ulong),
                ("dwTotalPageFile", c_ulong),
                ("dwAvailPageFile", c_ulong),
                ("dwTotalVirtual", c_ulong),
                ("dwAvailVirtual", c_ulong)
            ]
        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))

        return int(memoryStatus.dwAvailPhys/1024**2)
    else:
        raise NotImplementedError, "Will only work with Linux or Windows"



import array
class frozenarray(array.array):
    def __init__(self, typecode, initializer = []):
        array.array.__init__(self, typecode, initializer)

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(tuple(self))
            return self._hash
