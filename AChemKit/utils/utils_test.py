"""
This is the test harness for :py:mod:`AChemKit.utils.utils`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest
import random

from utils import *

__module__ = "AChemKit.sims_simple_test"

class TestGetSample(unittest.TestCase):
    
    def test_ints(self):
        result = get_sample(1)
        self.assertEqual(result, 1)
        result = get_sample(1.0)
        self.assertEqual(result, 1.0)
        result = get_sample(1, random.Random())
        self.assertEqual(result, 1)
        result = get_sample(1.0, random.Random())
        self.assertEqual(result, 1.0)
        
    def test_lists(self):
        result = get_sample([1,1,1])
        self.assertEqual(result, 1)
        result = get_sample([1,1,1], random.Random())
        self.assertEqual(result, 1)
        
    def test_dicts(self):
        result = get_sample({1:10})
        self.assertEqual(result, 1)
        result = get_sample({1:10}, random.Random())
        self.assertEqual(result, 1)

class TestFrozenBag(unittest.TestCase):
    
    strrep = "FrozenBag((1, 1, 2, 3))"
    cls = FrozenBag
    
    def setUp(self):
        self.data = (1,2,1,3)
        self.bag = self.cls(self.data)
        self.bag2 = self.cls(reversed(self.data))
        self.bag3 = self.cls(self.data+self.data)
        
    def test_len(self):
        self.assertEqual(len(self.bag), len(self.data))
        
    def test_iter(self):
        for a,b in zip(self.bag, sorted(self.data)):
            self.assertEqual(a, b)
        
    def test_hash(self):
        self.assertEqual(hash(self.bag), hash(self.bag2))
        
    def test_str(self):
        self.assertEqual(str(self.bag), self.strrep)
        
    def test_repr(self):
        self.assertEqual(repr(self.bag), self.strrep)

class TestBag(TestFrozenBag):
    
    strrep = "Bag([1, 1, 2, 3])"
    cls = Bag
    
        
    def setUp(self):
        self.data = [1,2,1,3]
        self.bag = self.cls(self.data)
        self.bag2 = self.cls(reversed(self.data))
        self.bag3 = self.cls(self.data+self.data)
        
    def test_hash(self):
        self.assertRaises(TypeError, hash, self.bag)
        
    def test_add(self):
        self.bag.add(4)
        self.assertEqual(self.bag, self.cls(reversed(self.data+[4])))
        
    def test_discard(self):
        self.bag.discard(2)
        self.data.remove(2)
        self.assertEqual(self.bag, self.cls(reversed(self.data)))

class TestOrderedFrozenBag(TestFrozenBag):
    
    strrep = "OrderedFrozenBag((1, 2, 1, 3))"
    cls = OrderedFrozenBag
    
    def setUp(self):
        super(TestOrderedFrozenBag, self).setUp()
        
    def test_iter(self):
        for a,b in zip(self.bag, self.data):
            self.assertEqual(a, b)

class TestOrderedBag(TestOrderedFrozenBag, TestBag):
    
    strrep = "OrderedBag([1, 2, 1, 3])"
    cls = OrderedBag

    def setUp(self):
        super(TestOrderedBag, self).setUp()
