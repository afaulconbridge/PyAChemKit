
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

from AChemKit.reactionnet import ReactionNetwork

import unittest

__module__ = "AChemKit.reactionnet_test"

class TestReactionNetwork(unittest.TestCase):

    def test_from_rates(self):
        rates = {(("A",), ("B",)):2.0}
        net = ReactionNetwork(rates)
        self.assertEqual(net.seen, ("A", "B"))
        self.assertEqual(net.reactions, ((("A",), ("B",)),))

if __name__=="__main__":
    unittest.main()