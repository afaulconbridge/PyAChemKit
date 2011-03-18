"""
The purpose of this is to see the coverage of the unit tests, so they can be
added to accordingly. It uses unittest2 to do this as well as coverage script
from nedbatchelder.com/code/coverage
"""


import unittest2 as unittest

if __name__ == "__main__":
    for match in unittest.defaultTestLoader.discover("AChemKit", pattern="*_test.py"):
        print match
        #TODO actually run the tests we find
    print "rununittest.py Done"