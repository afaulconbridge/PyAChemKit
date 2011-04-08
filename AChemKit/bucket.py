"""
Library for working with :py:class:`~.Bucket` objects; instances of a simulation of an Artificial Chemistry. 

Various tools for going between :py:class:`~.ReactionNetwork` and :py:class:`~.Bucket` objects, as well an analysing 
the data within :py:class:`~.Bucket` objects.
"""

import re
import collections

from .reactionnet import ReactionNetwork
from .utils.bag import OrderedFrozenBag

class Event(object):
    """
    Mini-class for tracking events (instances of a reaction) within a :py:class:`~.Bucket`.

    Supports comparisons, is hashable, is immutable.
    """

    def __init__(self, time, reactants, products):
        self.time = time
        self.reactants = OrderedFrozenBag(reactants)
        self.products = OrderedFrozenBag(products)

    def __eq__(self, other):
        if self.time == other.time and self.reactants == other.reactants and self.products == other.products:
            return True
        return False

    def __lt__(self, other):
        if self.time < other.time:
            return True
        return False

    def __hash__(self):
        if self._hash == None:
            self._hash = hash(self.time) + hash(self.reactants) + hash(self.products)
        return self._hash

class Bucket(object):
    """
    Event history of a simulation of an Artificial Chemistry.
    """
    _reactionnet = None
    events = []

    def __init__(self, events):
        self.events = []
        for event in events:
            if not isinstance(event, Event):
                event = Event(*event)
            self.events.append(event)
        self.events.sort()
        self.events = tuple(self.events)

    @classmethod
    def from_string(cls, instr):
        """
        Wrapper around :py:meth:`~.from_file` that uses :py:class:`~StringIO.StringIO`.
        """
        return cls.from_file(StringIO.StringIO(instr))

    @classmethod
    def from_filename(cls, infilename):
        """
        Wrapper around :py:meth:`~.from_file` that opens the provided filename as a file to read.
        """
        return cls.from_file(open(infilename, "r"))

    @classmethod
    def from_file(cls, file):
        """
        Alternative constructor that accepts a :py:func:`file` object (or equivalent).

        Source must be formatted as a bucket log  file, see :ref:`bucket_file_format`.
        """
        events = []
        for line in file:
            line = line.strip()
            
            splitted = line.split()
            if len(splitted) < 3:
                raise ValueError, "invalid reaction: "+reaction
            
            walltime = splitted[0]
            simtime = splitted[1]
            reaction = " ".join(splitted[2:])
            
            walltime = int(walltime)
            simtime = float(simtime)

            match = re.search(r"^(.*?)->(.*?)$", reaction)
            
            if match == None:
                raise ValueError, "invalid reaction: "+reaction
                
            reactants, products = match.groups()

            reactants = reactants.split("+")
            reactants = tuple( x.strip() for x in reactants if len(x.strip()) > 0 )

            products = products.split("+")
            products = tuple( x.strip() for x in products if len(x.strip()) > 0 )

            for reactant in reactants:
                assert " " not in reactant
                assert "\t" not in reactant
                assert "->" not in reactant
            for product in products:
                assert " " not in product
                assert "\t" not in product
                assert "->" not in product

            event = Event(simtime, reactants, products)
            events.append(event)
        return cls(events)

    @property
    def reactionnet(self):
        """
        A property that generates and caches a :py:class:`~.ReactionNetwork` object
        representing the reaction network exhibited by this bucket.
        
        Rates are calculated based on repeats of events in this bucket. This may have a large sampling
        error depending on how many repeates there were.
        """
        if self._reactionnet == None:
            #need to create a rates structure, then convert it to a reactionnet
            rates = {}
            seenreactants = {}
            
            for event in self.events:
                reactants = event.reactants
                products = event.products
                reaction = (reactants, products)
                if reaction not in rates:
                    rates[reaction] = 0
                rates[reaction] += 1
                
                reactants_sorted = tuple(sorted(reactants))
                if reactants_sorted not in seenreactants:
                    seenreactants[reactants_sorted] = 0
                seenreactants[reactants_sorted] += 1
                #if event.reactants == event.products:
                #    print "Bounce"
                
            #should correct the rates by the total number of collisions of those reactants
            #BUT current old data does not track bounces :`(
            
            #correct the rate by the number of times this occured
            for reaction in tuple(rates.keys()):
                reactants, products = reaction
                reactants_sorted = tuple(sorted(reactants))
                #print reaction, rates[reaction], seenreactants[reactants_sorted]
                assert float(rates[reaction]) <= float(seenreactants[reactants_sorted])
                rates[reaction] = float(rates[reaction]) / float(seenreactants[reactants_sorted])
                
            #remove bounces
            for reaction in tuple(rates.keys()):
                reactants, products = reaction
                if reactants == products:
                    del rates[reaction]

            self._reactionnet = ReactionNetwork(rates)

        return self._reactionnet
