"""
This is the test harness for :py:mod:`AChemKit.randomnet`.

Tricky to test well because it is non-deterministic.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest

from AChemKit.randomnet import Uniform, Linear
import random

__module__ = "AChemKit.randomnetnet_test"

class TestUniform(unittest.TestCase):
    
    def setUp(self):
        self.rng = random.Random(42)
        self.mols = ('M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9')
        
    def test_nmols_int(self):
        net = Uniform(10, 20, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nmols_tuple(self):
        net = Uniform(self.mols, 20, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nmols_list(self):
        net = Uniform(list(self.mols), 20, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        

class TestLinear(unittest.TestCase):
    
    def setUp(self):
        self.rng = random.Random(42)
