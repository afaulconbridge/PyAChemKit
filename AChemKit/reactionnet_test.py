
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

from AChemKit.reactionnet import ReactionNetwork

import unittest

__module__ = "AChemKit.reactionnet_test"

class TestReactionNetwork(unittest.TestCase):
    def setUp(self):
        rates = {(("A", "B"), ("B", "C")):2.0}
        self.net = ReactionNetwork(rates)

    def test_seen(self):
        self.assertEqual(self.net.seen, ("A", "B", "C"))
    def test_reactions(self):
        self.assertEqual(self.net.reactions, ((("A", "B"), ("B", "C")),))
    def test_rates(self):
        self.assertEqual(self.net.rates[("A", "B"), ("B", "C")], 2.0)
    def test_reaction_to_string(self):
        self.assertEqual(self.net.reaction_to_string((("A", "B"), ("B", "C")), 2.0), "A + B\t-2.0>\tB + C")
    
        

class TestReactionNetwork_from_string(TestReactionNetwork):
    def setUp(self):
        instring = "A + B -2.0>\tC +\tB"
        #this string includes:
        #  different kinds of whitespace
        #  disordered products
        #  floating-point rate
        self.net = ReactionNetwork.from_string(instring)
    

if __name__=="__main__":
    unittest.main()
