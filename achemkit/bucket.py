"""
Library for working with :py:class:`~.Bucket` objects; instances of a simulation of an Artificial Chemistry. 

Various tools for going between :py:class:`~.ReactionNetwork` and :py:class:`~.Bucket` objects, as well an analysing 
the data within :py:class:`~.Bucket` objects.
"""

import re
import collections
import math

from achemkit import ReactionNetwork
from achemkit import OrderedFrozenBag

class Event(object):
    """
    Mini-class for tracking events (instances of a reaction) within a :py:class:`~.Bucket`.

    Supports comparisons, is hashable, is immutable.
    """
    __slots__ = ["time", "reactants", "products", "rateconstant"]


    def __init__(self, time, reactants, products, rateconstant=None):
        reactants = OrderedFrozenBag(reactants)
        products = OrderedFrozenBag(products)
            
        #have to do it this way to avoid immutability issues
        super(Event, self).__setattr__('time', time)
        super(Event, self).__setattr__('reactants', reactants)
        super(Event, self).__setattr__('products', products)
        super(Event, self).__setattr__('rateconstant', rateconstant)

    def __repr__(self):
        return "Event({0},{1},{2},{3})".format(self.time, self.reactants, self.products, self.rateconstant)

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
        
    def __setattr__(self, name, value):
        raise TypeError("Cannot change an immutable object")
    def __delattr__(self):
        raise TypeError("Cannot change an immutable object")

class Bucket(object):
    """
    Event history of a simulation of an Artificial Chemistry.
    """
    _reactionnet = None
    events = []

    def __init__(self, events):
        """
        events will immediately be converted to a sorted tuple. If events is an 
        intterator this will cause it to be fully evaluated.
        """
        self.events = sorted(events)

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

            match = re.search(r"^(.*?)-([0-9]*\.?[0-9]*)>(.*?)$", reaction)
            
            if match == None:
                raise ValueError, "invalid reaction: "+reaction
                
            reactants, rateconstant, products = match.groups()

            reactants = reactants.split("+")
            reactants = tuple( x.strip() for x in reactants if len(x.strip()) > 0 )

            if rateconstant == "":
                rateconstant = None
            else:
                rateconstant = float(rateconstant)

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

            event = Event(simtime, reactants, products, rateconstant)
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
                if event.rateconstant is None:
                    if reaction not in rates:
                        rates[reaction] = 0
                    rates[reaction] += 1
                else:
                    if reaction not in rates:
                        rates[reaction] = event.rateconstant
                    else:
                        assert rates[reaction] == event.rateconstant
                
            self._reactionnet = ReactionNetwork(rates)

        return self._reactionnet
        
    def get_mol_counts(self, initialcounts, timeinterval=1.0):
        """
        Return a dictionary of dictionaries where the first key is time points,
        the second key is molecular species, and the value is the number of 
        molecules of that species present at that time.
        """
        
        data = {}
        if isinstance(initialcounts, tuple) or isinstance(initialcounts, list):
            data[0.0] = {}
            for mol in initialcounts:
                if mol not in data[0.0]:
                    data[0.0][mol] = 0
                data[0.0][mol] += 1
        elif isinstance(initialcounts, dict):
            data[0.0] = initialcounts
            
        def get_last_amount(data, mol):
            history = [x for x in data if x < time and mol in data[x]]
            if len(history) == 0:
                return 0
            else:
                lasttime = max([x for x in data if x < time and mol in data[x]])
                return data[lasttime][mol]
            
        for event in self.events:
            #assume that events is already sorted by increasing time
            time = (math.ceil(event.time/timeinterval))*timeinterval
            assert time > 0.0
            
            if time not in data:
                data[time] = {}
                
            for mol in event.reactants:
                if mol not in data[time]:
                    #get last known quantity
                    data[time][mol] = get_last_amount(data, mol)
                data[time][mol] -= 1
                
            for mol in event.products:
                if mol not in data[time]:
                    #get last known quantity
                    data[time][mol] = get_last_amount(data, mol)
                data[time][mol] += 1
                
        return data
