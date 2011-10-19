"""
This is the test harness for :py:mod:`achemkit.reactionnetdot`.

"""

import unittest

from achemkit import ReactionNetwork, net_to_dot

class TestReactionNetworkDot(unittest.TestCase):
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
        
    def test_to_dot_str(self):
        """
        Test for dot conversion by string representation
        
        Assumes that the dot representation itself is valid
        """
        target = 'digraph G {\n\tnode [margin="0.02,0.02", fontsize=10.0, width=0.3, height=0.0];\n\tedge [len=0.25, dir="both"];\n\tgraph [K=0.25, overlap="false"];\n\tM0 [label="A"];\n\tM1 [label="B"];\n\tM2 [label="C"];\n\tR0 [style="filled", label=2.0, width="0.2", shape="box", fillcolor="black", fontcolor="white", height="0.2", margin="0.01,0.01"];\n\tM0 -> R0 [arrowhead="none", arrowtail="invempty"];\n\tM1 -> R0 [color="grey", arrowhead="none", arrowtail="none"];\n\tR0 -> M2 [arrowhead="normal", arrowtail="none"];\n}'
        str(net_to_dot(self.net))
        #self.assertEqual(str(self.net.dot), target)
        
        
