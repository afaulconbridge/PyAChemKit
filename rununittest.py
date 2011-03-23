"""
The purpose of this is to see the coverage of the unit tests, so they can be
added to accordingly. It uses unittest to do this as well as coverage script
from nedbatchelder.com/code/coverage
"""

from unittest import TestSuite, TestLoader, TextTestRunner

#import all the stuff we expect users to use    
#from AChemKit import *
#from AChemKit.utils import *
#from AChemKit.tools import *

#import the test harnessess for particular classes
from AChemKit import reactionnet_test
from AChemKit import randomnet_test

if __name__ == "__main__":
    #because we want coverage, we do not want to auto-discover tests!
    suite = TestSuite()
    loader = TestLoader()
    
    suite.addTest(loader.loadTestsFromTestCase(reactionnet_test.TestReactionNetwork))
    suite.addTest(loader.loadTestsFromTestCase(reactionnet_test.TestReactionNetwork_from_string))
        
    suite.addTest(loader.loadTestsFromTestCase(randomnet_test.TestUniform))
    suite.addTest(loader.loadTestsFromTestCase(randomnet_test.TestLinear))
    
    TextTestRunner(verbosity=2).run(suite)

