"""
This is the test harness for :py:mod:`AChemKit.utils.utils`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest
import random

from utils import *

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
