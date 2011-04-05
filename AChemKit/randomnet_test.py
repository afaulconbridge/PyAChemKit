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

class TestUniform(unittest.TestCase):
    
    def setUp(self):
        self.rng = random.Random(42)
        self.mols = ('M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9')
        
    def test_nmols_int(self):
        net = Uniform(10, 50, 2, 2)
        net = Uniform(10, 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nmols_tuple(self):
        net = Uniform(self.mols, 50, 2, 2)
        net = Uniform(self.mols, 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nmols_list(self):
        net = Uniform(list(self.mols), 50, 2, 2)
        net = Uniform(list(self.mols), 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nmols_dict(self):
        mols = dict(zip(self.mols, range(1,len(self.mols)+1)))
        net = Uniform(mols, 50, 2, 2)
        net = Uniform(mols, 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nreacts_int(self):
        net = Uniform(10, 50, 2, 2)
        net = Uniform(10, 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nreacts_tuple(self):
        net = Uniform(10, 50, (1,2,2), 2)
        net = Uniform(10, 50, (1,2,2), 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nreacts_list(self):
        net = Uniform(10, 50, [1,2,2], 2)
        net = Uniform(10, 50, [1,2,2], 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nreacts_dict(self):
        net = Uniform(10, 50, {1:1, 2:2.0}, 2)
        net = Uniform(10, 50, {1:1, 2:2.0}, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
        
    def test_nprods_int(self):
        net = Uniform(10, 50, 2, 2)
        net = Uniform(10, 50, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nprods_tuple(self):
        net = Uniform(10, 50, 2, (1,2,2))
        net = Uniform(10, 50, 2, (1,2,2), rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nprods_list(self):
        net = Uniform(10, 50, 2, [1,2,2])
        net = Uniform(10, 50, 2, [1,2,2], rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nprods_dict(self):
        net = Uniform(10, 50, 2, {1:1, 2:2})
        net = Uniform(10, 50, 2, {1:1, 2:2}, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nprods_none_tuple(self):
        net = Uniform(10, 50, ((1,1), (2,2), (2,2)), None)
        net = Uniform(10, 50, ((1,1), (2,2), (2,2)), None, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_nprods_none_dict(self):
        net = Uniform(10, 50, {(1,1):1, (2,2):2.0}, None)
        net = Uniform(10, 50, {(1,1):1, (2,2):2.0}, None, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
        
    def test_rate_int(self):
        net = Uniform(10, 50, 2, 2, 2)
        net = Uniform(10, 50, 2, 2, 2, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_rate_float(self):
        net = Uniform(10, 50, 2, 2, 2.5)
        net = Uniform(10, 50, 2, 2, 2.5, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
    def test_rate_list(self):
        net = Uniform(10, 50, 2, 2, [1, 2.5, 3])
        net = Uniform(10, 50, 2, 2, [1, 2.5, 3], rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_rate_tuple(self):
        net = Uniform(10, 50, 2, 2, (1, 2.5, 3))
        net = Uniform(10, 50, 2, 2, (1, 2.5, 3), rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
    def test_rate_dict(self):
        net = Uniform(10, 50, 2, 2, {1:1, 1.0:1, 2.5:2.5})
        net = Uniform(10, 50, 2, 2, {1:1, 1.0:1, 2.5:2.5}, rng = self.rng)
        self.assertEqual(net.seen, self.mols)
        
        

class TestLinear(unittest.TestCase):
    
    def setUp(self):
        self.rng = random.Random(42)

    def test_natoms_int(self):
        net = Linear(2, 3, 0.2, 0.2)
        net = Linear(2, 3, 0.2, 0.2, rng = self.rng)
    def test_natoms_tuple(self):
        net = Linear((2,3), 3, 0.2, 0.2)
        net = Linear((2,3), 3, 0.2, 0.2, rng = self.rng)
    def test_natoms_dict(self):
        net = Linear({2:2,3:2.1}, 3, 0.2, 0.2)
        net = Linear({2:2,3:2.1}, 3, 0.2, 0.2, rng = self.rng)

    def test_maxlengt_tuple(self):
        net = Linear(2, (3,5), 0.2, 0.2)
        net = Linear(2, (3,5), 0.2, 0.2, rng = self.rng)
    def test_maxlengt_dict(self):
        net = Linear(2, {3:2,5:2.1}, 0.2, 0.2)
        net = Linear(2, {3:2,5:2.1}, 0.2, 0.2, rng = self.rng)

    def test_pform_tuple(self):
        net = Linear(2, (3,5), (0.2, 0.5), 0.2)
        net = Linear(2, (3,5), (0.2, 0.5), 0.2, rng = self.rng)

    def test_pbreak_tuple(self):
        net = Linear(2, (3,5), 0.2, (0.2, 0.5))
        net = Linear(2, (3,5), 0.2, (0.2, 0.5), rng = self.rng)

    def test_undirected(self):
        net = Linear(2, 3, 0.2, 0.2, False)
        net = Linear(2, 3, 0.2, 0.2, False, rng = self.rng)

    def test_directed(self):
        net = Linear(2, 3, 0.2, 0.2, True)
        net = Linear(2, 3, 0.2, 0.2, True, rng = self.rng)
