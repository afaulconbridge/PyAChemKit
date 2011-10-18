"""
This is the test harness for :py:mod:`AChemKit.sims_simple`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest
import random

import achemkit
from achemkit import OrderedFrozenBag

        
class TestItterative(unittest.TestCase):
    
    def setUp(self): 
        #self.net = randomnet.Uniform(5, 10, (1,2), (1,2))
        self.rates = {(achemkit.OrderedFrozenBag(["A", "B"]), OrderedFrozenBag(["B", "C"])):0.1}
        self.net = achemkit.ReactionNetwork(self.rates)
        self.mols = [mol for mol in self.net.seen*10]
        self.achem = achemkit.AChemReactionNetwork(self.net)
        
        
    def test_basic(self):
        #this isnt a complete test, but it runs some code and gets a result
        events = achemkit.sim_itterative(self.achem, self.mols, 10)
        buck = achemkit.Bucket(events)
        self.assertEqual(set(buck.reactionnet.reactions), set(self.net.reactions))

class TestStepwise(TestItterative):
        
    def test_basic(self):
        #this isnt a complete test, but it runs some code and gets a result
        events = achemkit.sim_stepwise(self.achem, self.mols, 10)
        buck = achemkit.Bucket(events)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
        
class TestEnumerate(TestItterative):
        
    def test_basic(self):
        #this isnt a complete test, but it runs some code and gets a result
        events = achemkit.sim_enumerate(self.achem, set(self.mols), 10)
        buck = achemkit.Bucket(events)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
        
if __name__=="__main__":
    unittest.main()
