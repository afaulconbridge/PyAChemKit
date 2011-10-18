import random

from achemkit import OrderedFrozenBag

class AChem(object):

    def react(self, molecules):
        """
        May be implemented by subclasses to enable simulation
        of reaction network.
        
        Give one or more molecules, returns a collection of products.
        
        Elastic reactions return the sample products as reactants.
        """
        raise NotImplementedError
        
        
    def all_reactions(self, molecules):
        """
        May be implemented by subclasses to enable enumeration
        of reaction network.
        
        Given one or more molecules, returns a dictionary where
        keys are possible reaction products and values are relative
        frequencies.
        """
        raise NotImplementedError
        
        
    def atoms(self, molecule):
        """
        May be implemented by subclasses to enable some analysis
        techniques.
        
        Given a molecule, returns an itterable over all atoms in that
        molecule.
        """
        raise NotImplementedError
        
       
class AChemReactionNetwork(AChem):
    """
    This is an AChem class that uses a Reaction Network as its base. 
    
    The main point of this is to be able to compare different simuatlion
    approaches to see which ones best reconstruct the original Reaction 
    Network.
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
