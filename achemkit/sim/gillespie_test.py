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

class TestGillespie(unittest.TestCase):
    
    def setUp(self): 
        #self.net = randomnet.Uniform(2, 2, (1,2), (1,2))
        self.rates = {(OrderedFrozenBag(["A", "B"]), OrderedFrozenBag(["B", "C"])):0.1}
        self.net = achemkit.ReactionNetwork(self.rates)
        self.mols = [mol for mol in self.net.seen*10]
        self.achem = achemkit.AChemReactionNetwork(self.net)
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        events = achemkit.sim_gillespie(self.achem, self.mols, 50, random.Random())
        buck = achemkit.Bucket(events)
        print self.net
        print "-"*25
        print str(buck.reactionnet)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
        self.assertEqual(1,1)

