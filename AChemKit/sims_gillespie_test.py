"""
This is the test harness for :py:mod:`AChemKit.sims_simple`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest
import random

import sims_simple
import sims_gillespie
import reactionnet
import randomnet
import bucket

class TestGillespie(unittest.TestCase):
    
    def setUp(self): 
        self.net = randomnet.Uniform(2, 2, (1,2), (1,2))
        self.mols = [mol for mol in self.net.seen*10]
        self.achem = sims_simple.AChemReactionNetwork(self.net)
        
    def test_basic(self):
        #this isnt a true test, but it runs some code and gets a result
        events = sims_gillespie.simulate_gillespie(self.achem, self.mols, 10, random.Random())
        buck = bucket.Bucket(events)
        print self.net
        print "-"*25
        print str(buck.reactionnet)
        self.assertEqual(buck.reactionnet.reactions, self.net.reactions)
        self.assertEqual(1,1)
        
