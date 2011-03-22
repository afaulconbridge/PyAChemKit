"""
This is the test harness for ``reactionnet.py``.
"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest as unittest

from AChemKit.reactionnet import ReactionNetwork

__module__ = "AChemKit.reactionnet_test"

class TestReactionNetwork(unittest.TestCase):
    """
    This is the main class to test ReactionNetwork class. 
    
    It relies on setUp to generate a ReactionNetwork instance which
    is then probed by the test_ functions
    """
    def setUp(self): 
        rates = {(("A", "B"), ("B", "C")):2.0}
        self.net = ReactionNetwork(rates)

    def test_seen(self):
        """
        Makes sure the molecules that were specified are in seen.
        Also checks that they are in sorted order.
        """
        self.assertEqual(self.net.seen, ("A", "B", "C"))
        
    def test_reactions(self):
        """
        Makes sure the reactions that were specified are in reactions.
        Also checks that they are in sorted order
        TODO check sorted order between reactions
        """
        self.assertEqual(self.net.reactions, ((("A", "B"), ("B", "C")),))
        
    def test_rates(self):
        self.assertEqual(self.net.rates[("A", "B"), ("B", "C")], 2.0)
        
    def test_reaction_to_string(self):
        """
        Check that it convert a reaction to a string correctly
        """
        target = """A + B\t-2.0>\tB + C"""
        self.assertEqual(self.net.reaction_to_string((("A", "B"), ("B", "C")), 2.0), target)
        
    def test_to_string(self):
        """
        Check that it converts to a string correctly
        """
        target = """A + B\t-2.0>\tB + C"""
        self.assertEqual(str(self.net), target)

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
