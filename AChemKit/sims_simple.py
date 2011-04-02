
import random
try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle
    
from utils.utils import get_sample

class AChemAbstract(object):
    """
    This is an abstract base class for an AChem that can be used in a 
    simulation or similar. It defines core attribtues and functions
    that subclasses must implement in order to follow the API correctly.
    
    It is not required that an AChem inherits this, as Python follows
    the principle of "duck typing".
    """
    
    """
    The number of reactants in each reaction.
    
    Can be an int, a list or tuple (which will be selected for with equal 
    probability; repeats allowed), or a dict (where keys are possible 
    number of reactants and values are int or float weights).
    """
    noreactants = 2 
    
    
    def __init__(self):
        pass

    def react(self, *reactants):
        """
        Given some number of reactants, return the products.
        
        The reactant objects should not be changed. Rather, copies should
        be returned. This is so events and buckets work correctly.
        """
        return reactants
        
class AChemReactionNetwork(AChemAbstract):
    """
    This is an AChem class that uses a Reaction Network as its base. 
    
    The main point of this is to be able to compare different simuatlion
    approaches to see which ones best reconstruct the original Reaction 
    Network.
    """
    
    def __init__(self, reactionnetwork):
        self.reactionnetwork = reactionnetwork
        self.noreactants = [len(x) for x,y in reactionnetwork.reactions]
        
    def react(self, *reactants):
        possibleproducts = []
        for netreactants, netproducts in self.reactionnetwork.reactions:
            if netreactants == reactants:
                possibleproducts.append(netproducts)
        if len(possibleproducts) == 0:
            return reactants
        else:
            return random.choice(possibleproducts)
     

def simulate_itterative_iter(achem, mols, maxtime, rng = None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. It returns events as tuples of (time, reactants, products).
    
    One reaction occurs each second for a number of seconds up to the 
    maximum time specified.
    
    Works as an iterator to reduce memory consumption. See simulate_itterative
    for this function wrapped in a tuple.
    """
    
    mols = tuple(mols)
    if rng is None:
        rng = random.Random()
    
    time = 0.0
    while time < maxtime:
        mols = tuple(rng.sample(mols, len(mols)))
        
        noreactants = get_sample(achem.noreactants, rng)
        reactants = mols[:noreactants]
        mols = mols[noreactants:]
        
        products = tuple(achem.react(*reactants))
        mols += products
        
        yield (time, reactants, products)
        
        time += 1.0
        
    raise StopIteration
    
def simulate_itterative(achem, mols, maxtime, rng=None):
    return tuple(simulate_itterative_iter(achem, mols, maxtime, rng))


def simulate_stepwise_iter(achem, mols, maxtime, rng=None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. It returns events as tuples of (time, reactants, products).
    
    Each molecule will attempt to react once for each second. If there 
    are any leftover molecules, they will get a free pass to the next 
    second.
    
    Is an iterator to reduce memory consumption. See simulate_stepwise
    for this function wrapped in a tuple.
    """
    
    mols = tuple(mols)
    if rng is None:
        rng = random.Random()
    
    time = 0.0
    while time < maxtime:
        mols = tuple(rng.sample(mols, len(mols)))
        newmols = ()
        while len(mols) > 0:
            noreactants = get_sample(achem.noreactants, rng)
            if noreactants <= len(mols):
                reactants = mols[:noreactants]
                mols = mols[noreactants:]
                
                products = achem.react(*reactants)
                newmols += products
                #reactants = tuple(str(reactant) for reactant in reactants)
                #products = tuple(str(product ) for product in products)
                
                yield (time, reactants, products)
            else:
                newmols += mols
                mols = ()
        mols = newmols
        time += 1.0
        
    raise StopIteration

def simulate_stepwise(achem, mols, maxtime, rng=None):
    return tuple(simulate_stepwise_iter(achem, mols, maxtime, rng))


def simulate_stepwise_multiprocessing_iter(achem, mols, maxtime, rng=None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. It returns events as tuples of (time, reactants, products).
    
    Each molecule will attempt to react once for each second. If there 
    are any leftover molecules, they will get a free pass to the next 
    second.
    
    Is an iterator to reduce memory consumption. See simulate_stepwise_multiprocessing
    for this function wrapped in a tuple.
    
    Uses multiprocessing to parallelize reactions. This does not work
    that well because the individual reactions are not that complicated.
    """
    for mol in mols:
        pickle.dumps(mol)
    pickle.dumps(achem)
    pickle.dumps(achem.react)
    
    import math
    import multiprocessing
    p = multiprocessing.Pool()
    
    mols = tuple(mols)
    if rng is None:
        rng = random.Random()
    
    time = 0.0
    while time < maxtime:
        mols = tuple(rng.sample(mols, len(mols)))
        newmols = ()
        allreactants = []
        while len(mols) > 0:
            noreactants = get_sample(achem.noreactants, rng)
            if noreactants <= len(mols):
                reactants = mols[:noreactants]
                mols = mols[noreactants:]
                allreactants.append(reactants)
            else:
                newmols += mols
                mols = ()
                
        allproducts = p.imap_unordered(achem.react, allreactants)
        for reactants, products in zip(allreactants, allproducts):
            newmols += products
            #reactants = tuple(str(reactant) for reactant in reactants)
            #products = tuple(str(product ) for product in products)
            
            yield (time, reactants, products)
        mols = newmols
        time += 1.0
    p.terminate()
    p.close()
    raise StopIteration

def simulate_stepwise_multiprocessing(achem, mols, maxtime, rng=None):
    return tuple(simulate_stepwise_multiprocessing_iter(achem, mols, maxtime, rng))
