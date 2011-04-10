"""
This is the test harness for :py:mod:`AChemKit.reactionnetdot`.

"""
#this will not be required once a proper installer exists
import sys
sys.path.append(".")

import unittest

from reactionnetdot import ReactionNetworkDot

class TestReactionNetworkDot(unittest.TestCase):
    """
    This is the main class to test ReactionNetwork class. 
    
    It relies on setUp to generate a ReactionNetwork instance which
    is then probed by the other functions
    """
    def setUp(self): 
        self.rates = {(("A", "B"), ("B", "C")):2.0}
        self.net = ReactionNetworkDot(self.rates)
        
        self.othernet = ReactionNetworkDot(self.rates)
        
        self.wrongrates = {(("A", "B"), ("B", "C")):3.0}
        self.wrongnet = ReactionNetworkDot(self.wrongrates)
        
    def test_to_dot_str(self):
        """
        Test for dot conversion by string representation
        
        Assumes that the dot representation itself is valid
        """
        target = """digraph G {
	node [margin="0.02,0.02", fontsize=10.0, width=0.3, height=0.0];
	edge [len=0.25, dir="both"];
	graph [K=0.25, layout="sfdp", overlap="false"];
	M0 [label="A"];
	M1 [label="B"];
	M2 [label="C"];
	R0 [style="filled", label=2.0, width="0.0", shape="box", fillcolor="black", fontcolor="white", height="0.0", margin="0.01,0.01"];
	M0 -> R0 [arrowhead="none", arrowtail="invempty"];
	M1 -> R0 [color="grey", arrowhead="none", arrowtail="none"];
	R0 -> M2 [arrowhead="normal", arrowtail="none"];
}"""
        self.assertEqual(str(self.net.dot), target)
