import random
import itertools
try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle


import umpf
    
from achemkit.utils.utils import get_sample
from achemkit import OrderedFrozenBag
from achemkit.sim.sim import Reactor
from achemkit import Event

class ReactorEnumerate(Reactor):
    def __init__(self, achem, mols):
        super(ReactorEnumerate, self).__init__(achem, mols)
        self.maxmols = 0        
        self.mols = []
        self.tested = []
        self.untested = []
                
        for mol in mols:
            self.add_mol(mol)
            
    def add_mol(self, mol):
        if mol not in self.mols:
            self.mols.append(mol)
            for other in self.mols:
                reactants = OrderedFrozenBag((mol, other))
                assert reactants not in self.tested
                self.untested.append(reactants)
        
    def do(self, count):
        self.maxmols += count
        while len(self.mols) < self.maxmols and len(self.untested) > 0:
            untested = tuple(self.untested)
            self.untested = []
            results = itertools.izip(untested, umpf.map(self.achem.all_reactions, untested))
            while len(self.mols) < self.maxmols:
                try:
                    reactants, all_products = results.next()
                except StopIteration:
                    break
                else:
                    reactants = OrderedFrozenBag(reactants)
                    self.tested.append(reactants)
                    for products in all_products:
                        e = Event(0.0, reactants, products, all_products[products])
                        yield e
                        for product in products:
                            self.add_mol(product)

class ReactorItterative(Reactor):
    def __init__(self, achem, mols, rngseed=None):
        super(ReactorItterative, self).__init__(achem, mols)
        self.maxtime = 0.0
        self.time = 0.0
        if isinstance(rngseed, random.Random):
            self.rng = rngseed
        else:
            self.rng = random.Random(rngseed)
        
        
    def do(self, time):
        self.maxtime += time
        while self.time < self.maxtime:
            self.mols = tuple(self.rng.sample(self.mols, len(self.mols)))
            
            noreactants = 2
            reactants = OrderedFrozenBag(self.mols[:noreactants])
            self.mols = self.mols[noreactants:]
            
            products = self.achem.react(reactants)
            self.mols += tuple(products)
            
            e = Event(time, reactants, products)
            yield e
            
            self.time += 1.0
                
class ReactorStepwise(Reactor):
    def __init__(self, achem, mols, rngseed=None):
        super(ReactorStepwise, self).__init__(achem, mols)
        self.maxtime = 0.0
        self.time = 0.0
        if isinstance(rngseed, random.Random):
            self.rng = rngseed
        else:
            self.rng = random.Random(rngseed)
        
        
    def do(self, time):
        self.maxtime += time
        while self.time < self.maxtime:
            self.mols = tuple(self.rng.sample(self.mols, len(self.mols)))
            newmols = ()
            allreactants = []
            while len(self.mols) > 0:
                noreactants = 2
                if noreactants <= len(self.mols):
                    reactants = self.mols[:noreactants]
                    self.mols = self.mols[noreactants:]                
                    allreactants.append(OrderedFrozenBag(reactants))
                    
            allproducts = umpf.map(self.achem.react, allreactants)
            results = itertools.izip(allreactants, allproducts)
            for reactants, products in results:
                e = Event(time, reactants, products)
                newmols += tuple(products)
                yield e
                
            self.mols = newmols
            self.time += 1.0
            
def sim_enumerate(achem, mols, maxmols):
    """
    Given an Artificial Chemistry, this e numerates all possinle reactions. It 
    yields Event objects.
    
    Limited to a maximum number of molecular species.
    
    This is an iterator to reduce memory consumption.
    """
    sim = ReactorEnumerate(achem, mols)
    for e in sim.do(maxmols):
        yield e
        
def sim_itterative(achem, mols, maxtime, rng = None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. Yields Event objects.
    
    One reaction occurs each second for a number of seconds up to the 
    maximum time specified.
    
    This is an iterator to reduce memory consumption.
    """
    sim = ReactorItterative(achem, mols, rng)
    for e in sim.do(maxtime):
        yield e
    

def sim_stepwise(achem, mols, maxtime, rng=None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. Yields Event objects.
    
    Each molecule will attempt to react once for each second. If there 
    are any leftover molecules, they will get a free pass to the next 
    second.
    
    This is an iterator to reduce memory consumption. 
    
    Uses umpf for parallelism.
    """
    sim = ReactorStepwise(achem, mols, rng)
    for e in sim.do(maxtime):
        yield e

