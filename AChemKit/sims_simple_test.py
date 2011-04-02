"""
This is the test harness for :py:mod:`AChemKit.sims_simple`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest
import random

import sims_simple
import reactionnet
import randomnet

__module__ = "AChemKit.sims_simple_test"
        
class TestItterative(unittest.TestCase):
    
    def setUp(self): 
        self.rates = {(("A", "B"), ("B", "C")):2.0}
        self.net = reactionnet.ReactionNetwork(self.rates)
        self.net = randomnet.Uniform(10, 10, (1,2), (1,2))
        self.mols = ["A", "B", "B"]
        self.achem = sims_simple.AChemReactionNetwork(self.net)
        
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        a = sims_simple.simulate_itterative(self.achem, self.mols, 100)
        b = sims_simple.simulate_itterative(self.achem, self.mols, 100, random.Random())
        self.assertEqual(1,1)
        
class TestStepwise(TestItterative):
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        a = sims_simple.simulate_stepwise(self.achem, self.mols, 10)
        b = sims_simple.simulate_stepwise(self.achem, self.mols, 10, random.Random())
        self.assertEqual(1,1)
        
class TestStepwiseMultiprocessing(TestItterative):
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        a = sims_simple.simulate_stepwise_multiprocessing(self.achem, self.mols, 10)
        b = sims_simple.simulate_stepwise_multiprocessing(self.achem, self.mols, 10, random.Random())
        self.assertEqual(1,1)
    
if __name__=="__main__":
    unittest.main()
