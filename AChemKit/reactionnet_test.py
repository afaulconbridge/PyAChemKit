"""
This is the test harness for :py:mod:`AChemKit.reactionnet`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest

from reactionnet import ReactionNetwork

class TestReactionNetwork(unittest.TestCase):
    """
    This is the main class to test ReactionNetwork class. 
    
    It relies on setUp to generate a ReactionNetwork instance which
    is then probed by the other functions
    """
    def setUp(self): 
        self.rates = {(("A", "B"), ("B", "C")):2.0}
        self.net = ReactionNetwork(self.rates)
        
        self.othernet = ReactionNetwork(self.rates)
        
        self.wrongrates = {(("A", "B"), ("B", "C")):3.0}
        self.wrongnet = ReactionNetwork(self.wrongrates)

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
        
    def test_equal(self):
        """
        As ReactionNetwork has a custom __eq__ function, it is tested
        here.
        
        Needs to both pass and fail.
        """
        self.assertTrue(self.net != None)
        self.assertTrue(self.net != "SPAM!")
        self.assertEqual(self.net, self.othernet)
        self.assertTrue(self.net != self.wrongnet)
        
    def test_hash(self):
        """
        As ReactionNetwork has a custom __hash__ function, it is tested
        here.
        
        Needs to both pass and fail.
        
        Technically, the fail here could be true and still be a hash
        but it is supposed to usually be wrong so assume that it will be
        wrong.
        """
        self.assertEqual(hash(self.net), hash(self.othernet))
        #technically, this could be true and still be a hash
        #but it is supposed to usually be wrong
        self.assertTrue(hash(self.net) != hash(self.wrongnet))

class TestReactionNetwork_from_string(TestReactionNetwork):
    def setUp(self):
        self.instring = "A + B -2.0>\tC +\tB"
        #this string includes:
        #  different kinds of whitespace
        #  disordered products
        #  floating-point rate
        self.net = ReactionNetwork.from_string(self.instring)
        
        self.othernet = ReactionNetwork.from_string(self.instring)
        
        self.wrongstring = "A + B\t-3.0> C + B"
        self.wrongnet = ReactionNetwork.from_string(self.wrongstring)
    

if __name__=="__main__":
    unittest.main()
