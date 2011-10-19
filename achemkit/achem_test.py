import unittest

import achemkit
import achemkit.achem
from achemkit import OrderedFrozenBag

class TestAChem(unittest.TestCase):
    def setUp(self):        
        self.rates = {(OrderedFrozenBag(["A", "B"]), OrderedFrozenBag(["B", "C"])):2.0}
        self.net = achemkit.ReactionNetwork(self.rates)
        self.achem = achemkit.AChemReactionNetwork(self.net)
        
    def test(self):
        self.assertEqual(self.achem.react(("A", "B")), OrderedFrozenBag(("B", "C")))
