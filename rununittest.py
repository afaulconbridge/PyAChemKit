"""
The purpose of this is to see the coverage of the unit tests, so they can be
added to accordingly. It uses unittest to do this as well as coverage script
from nedbatchelder.com/code/coverage
"""

from unittest import TestSuite, TestLoader, TextTestRunner

    
#from coverage import coverage
#cov = coverage(cover_pylib=False)
#cov.start()

if __name__ == "__main__":
    #because we want coverage, we do not want to auto-discover tests!
    suite = TestSuite()
    loader = TestLoader()
    
    import AChemKit
    import AChemKit.reactionnet
    
    import AChemKit.reactionnet_test
    suite.addTest(loader.loadTestsFromTestCase(AChemKit.reactionnet_test.TestReactionNetwork))
    suite.addTest(loader.loadTestsFromTestCase(AChemKit.reactionnet_test.TestReactionNetwork_from_string))
    
    import AChemKit.bucket
    
    import AChemKit.randomnet
    
    TextTestRunner(verbosity=2).run(suite)

#cov.stop()
#cov.save()
