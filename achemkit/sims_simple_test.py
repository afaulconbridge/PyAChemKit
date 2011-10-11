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
import bucket
from utils.bag import OrderedFrozenBag

        
class TestItterative(unittest.TestCase):
    
    def setUp(self): 
        #self.net = randomnet.Uniform(5, 10, (1,2), (1,2))
        self.rates = {(OrderedFrozenBag(["A", "B"]), OrderedFrozenBag(["B", "C"])):0.1}
        self.net = reactionnet.ReactionNetwork(self.rates)
        self.mols = [mol for mol in self.net.seen*10]
        self.achem = sims_simple.AChemReactionNetwork(self.net)
        
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        events = sims_simple.simulate_itterative(self.achem, self.mols, 100)
        buck = bucket.Bucket(events)
        self.assertEqual(set(buck.reactionnet.reactions), set(self.net.reactions))

class TestStepwise(TestItterative):
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        events = sims_simple.simulate_stepwise(self.achem, self.mols, 100)
        buck = bucket.Bucket(events)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
        
"""
#this is broken ATM
class TestStepwiseMultiprocessing(TestItterative):
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        events = sims_simple.simulate_stepwise_multiprocessing(self.achem, self.mols, 100, random.Random())
        buck = bucket.Bucket(events)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
"""

if __name__=="__main__":
    unittest.main()
