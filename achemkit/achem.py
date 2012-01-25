"""
This module contains a template for representing generic Artificial Chemistries,
without needing to explicit list all reactions. Whilst this is not required to
be used as a base class for custom Artificial Chemistries, it is recommended
to do so.
"""

import random

from achemkit import OrderedFrozenBag

class AChem(object):
    noreactants = (2,)

    def react(self, molecules):
        """
        May be implemented by subclasses to enable simulation
        of reaction network.
        
        Elastic reactions return the reactants as the products.
        
        :param molecules: Itterable of reactant molecules
        :rtype: Itterable of product molecules
        """
        raise NotImplementedError
        
        
    def all_reactions(self, molecules):
        """
        May be implemented by subclasses to enable enumeration
        of reaction network.
        
        Given one or more molecules, returns a dictionary where
        keys are possible reaction products and values are relative
        rate constants.
        
        :param molecules: Itterable of reactant molecular species
        :rtype: Dictionary with tuples of (reactants, products) as keys and
                rate constants as values.
        """
        raise NotImplementedError
        
        
    def atoms(self, molecule):
        """
        May be implemented by subclasses to enable some analysis
        techniques. Should only be implemented for Artificial Chemistries where
        molecules are composed of atoms (structured or sub-symbolic).
        
        Itterates over each atom wthin a molecule. 
        :param molecule: A molecule object
        :rtype: Itterable over atoms
        """
        raise NotImplementedError
        
       
class AChemReactionNetwork(AChem):
    """
    This is a subclass of :py:class:`AChem` that uses a 
    :py:class:`achem.Reaction Network` as its base. 
    
    This is designed to be used to compare different simulation approaches, 
    typically to see which best reconstructs the original
    :py:class:`achem.Reaction Network`.
    """
    
    def __init__(self, reactionnetwork):
        self.reactionnetwork = reactionnetwork
        self.noreactants = [len(x) for x,y in reactionnetwork.reactions]
        
    def react(self, reactants):
        #need to convert to a bag so that it maps to the reactionnetwork properly
        if not isinstance(reactants, OrderedFrozenBag):
            reactants = OrderedFrozenBag(reactants)
            
        possibleproducts = []
        for netreactants, netproducts in self.reactionnetwork.reactions:
            if netreactants == reactants:
                possibleproducts.append(netproducts)
                
        if len(possibleproducts) == 0:
            return reactants
        else:
            return random.choice(possibleproducts)
        
    def all_reactions(self, reactants):
        #need to convert to a bag so that it maps to the reactionnetwork properly
        reactants = OrderedFrozenBag(reactants)
            
        possibleproducts = {}
        for netreactants, netproducts in self.reactionnetwork.reactions:
            if netreactants == reactants:
                possibleproducts[netreactants, netproducts] =  self.reactionnetwork.rate(netreactants, netproducts)
        
        return possibleproducts
