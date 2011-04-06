"""
The purpose of this is to see the coverage of the unit tests, so they can be
added to accordingly. It uses unittest to do this as well as coverage script
from nedbatchelder.com/code/coverage
"""

from unittest import TestSuite, TestLoader, TextTestRunner

#import all the stuff we expect users to use    
from AChemKit import *
from AChemKit.utils import *
from AChemKit.tools import *

#import the test harnessess for particular classes
from AChemKit import reactionnet_test
from AChemKit import reactionnetdot_test
from AChemKit import randomnet_test
from AChemKit import sims_simple_test
from AChemKit import sims_gillespie_test
from AChemKit.utils import utils_test
from AChemKit.utils import bag_test



if __name__ == "__main__":
    #because we want coverage, we do not want to auto-discover tests!
    suite = TestSuite()
    loader = TestLoader()
    
    suite.addTest(loader.loadTestsFromTestCase(utils_test.TestGetSample))
    
    suite.addTest(loader.loadTestsFromTestCase(bag_test.TestFrozenBag))
    suite.addTest(loader.loadTestsFromTestCase(bag_test.TestBag))
    suite.addTest(loader.loadTestsFromTestCase(bag_test.TestOrderedFrozenBag))
    suite.addTest(loader.loadTestsFromTestCase(bag_test.TestOrderedBag))
    
    suite.addTest(loader.loadTestsFromTestCase(reactionnet_test.TestReactionNetwork))
    suite.addTest(loader.loadTestsFromTestCase(reactionnet_test.TestReactionNetwork_from_string))
    suite.addTest(loader.loadTestsFromTestCase(reactionnetdot_test.TestReactionNetworkDot))
        
    suite.addTest(loader.loadTestsFromTestCase(randomnet_test.TestUniform))
    suite.addTest(loader.loadTestsFromTestCase(randomnet_test.TestLinear))
        
    suite.addTest(loader.loadTestsFromTestCase(sims_simple_test.TestItterative))
    suite.addTest(loader.loadTestsFromTestCase(sims_simple_test.TestStepwise))
    suite.addTest(loader.loadTestsFromTestCase(sims_simple_test.TestStepwiseMultiprocessing))
    
    suite.addTest(loader.loadTestsFromTestCase(sims_gillespie_test.TestGillespie))
    
    TextTestRunner(verbosity=2).run(suite)
