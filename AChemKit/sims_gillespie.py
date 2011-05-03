
# -*- coding: UTF-8 -*-

import random

from . import sims_simple

def simulate_gillespie_iter(achem, mols, maxtime, rng=None):
    """
    Given an Artificial Chemistry, this simulates a series of simple
    iterative reactions. It returns events as tuples of (time, reactants, products).
    
    This is an implementation of the Gillespie algorithm. It is a simulation
    of a well-mixed container.
    
    Is an iterator to reduce memory consumption. See simulate_gillespie
    for this function wrapped in a tuple.
    """
    
    mols = tuple(mols)
    if rng is None:
        rng = random.Random()
    
    g = Gillespie(achem, mols, rng)
    
    time = 0.0
    while time < maxtime:
        
        interval, reactants, products = g.next_reaction()
        time += interval
        if reactants != None and products != None:
            yield (time, reactants, products)
        
    raise StopIteration

def simulate_gillespie(achem, mols, maxtime, rng=None):
    return tuple(simulate_gillespie_iter(achem, mols, maxtime, rng))

class Gillespie(object):
    
    def __init__(self, achem, mols, rng, intervalscaling = 100.0):
        self.achem = achem
        self.mols = mols
        self.rng = rng
        self.intervalscaling = intervalscaling #temperature/pressure analog
        
        self.possiblenoreactants = None
        if isinstance(self.achem.noreactants, int) or isinstance(self.achem.noreactants, float):
            self.possiblenoreactants = tuple((self.achem.noreactants,))
        elif isinstance(self.achem.noreactants, list) or isinstance(self.achem.noreactants, tuple):
            self.possiblenoreactants = tuple(sorted(list(self.achem.noreactants)))
        elif isinstance(self.achem.noreactants, dict):
            self.possiblenoreactants = tuple(sorted(list(self.achem.noreactants.keys())))
        else:
            raise ValueError, "cannot determine possible no's of reactants"

    def next_reaction(self):
        #Let the next reaction have index μ and fire at time t + τ.
        #Let α be the sum of the propensities.
        #The time to the next reaction is an exponentially distributed
        #random variable with mean 1 / α ; the probability density function
        #is P(τ = x) = α e- α x.
        #The index of the next reaction to fire is a discrete random
        #variable with probability mass function P(μ = m) = am / α.
        
        #assumes two reactants to a reaction
        totalnumberofreactions = 0
        for noreactants in self.possiblenoreactants:
            i = noreactants
            count = len(self.mols)
            if i <= len(self.mols):
                while i > 1:
                    count *= (len(self.mols)-(i-1))
                    i -= 1
            totalnumberofreactions += count
                        
        interval = self.rng.expovariate(float(totalnumberofreactions)) * self.intervalscaling

        noreactants = sims_simple.get_sample(self.achem.noreactants, self.rng)
        
        if len(self.mols) >= noreactants:
            self.mols = list(self.mols)
            self.rng.shuffle(self.mols)
            self.mols = tuple(self.mols)
            
            reactants = self.mols[:noreactants]
            self.mols = self.mols[noreactants:]

            products = tuple(self.achem.react(reactants))
            self.mols += products
            return interval, reactants, products
        else:
            return interval, None, None
