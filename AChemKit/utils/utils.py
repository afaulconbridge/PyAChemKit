"""
Various small functions that can get combined together.
"""

import random
import collections


def get_sample(distribution, rng=None):
    if rng is None:
        rng = random.Random()
    if isinstance(distribution, int) or isinstance(distribution, float):
        return distribution
    elif isinstance(distribution, list) or isinstance(distribution, tuple):
        return (rng.sample(distribution, 1))[0]
    elif isinstance(distribution, dict):
        #assume its a value:proportion dict
        total = sum(distribution.values())
        target = rng.random()*total
        i = 0
        score = distribution.values()[i]
        hit = distribution.keys()[i]
        while score < target:
            i += 1
            score += distribution.values()[i]
            hit = distribution.keys()[i]
        return hit


class FrozenBag(collections.Set):
    """
    A Bag is like a set, but can contain duplicates.
    
    Also, a Bag is like a list, but is always ordered.
    """
    _items = ()
    
    def __init__(self, itterable):
        self._items = tuple(sorted(list(itterable)))
        
    def __contains__(self, item):
        return item in self._items
        
    def __len__(self):
        return len(self._items)
        
    def __iter__(self):
        for item in self._items:
            yield item
        
    def __hash__(self):
        return hash(self._items)
        
    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        return "{0}({1})".format(str(self.__class__.__name__), repr(self._items))
    
    
class Bag(FrozenBag, collections.MutableSet):
    """
    A Bag is like a set, but can contain duplicates.
    
    Also, a Bag is like a list, but is always ordered.
    """
    
    _items = []
    
    def __init__(self, itterable):
        self._items = sorted(list(itterable))
        
    def add(self, item):
        self._items = sorted(self._items+[item])
        
    def discard(self, item):
        i = self._items.index(item)
        #no need to resort since it is in the same order
        self._items = self._items[:i]+self._items[i+1:]
        
    def __hash__(self):
        raise TypeError, "unhashable type: '{0}'".format(str(self.__class__.__name__))
        
class OrderedFrozenBag(collections.Set):
    """
    Like a FrozenBag, but iterating will keep the order things were put in.
    
    Comparisons are still as for a FrozenBag so OrderedFrozenBag([1,2,1]) == OrderedFrozenBag([2,1,1])
    will return True.
    """
    
    def __init__(self, itterable):
        self._order = tuple(itterable)
        self._bag = FrozenBag(self._order)
        
    def __contains__(self, item):
        return item in self._order
        
    def __len__(self):
        return len(self._order)
        
    def __iter__(self):
        for item in self._order:
            yield item
        
    def __hash__(self):
        return hash(self._bag)
        
    def __str__(self):
        return repr(self)
        
    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        print self.__class__.__name__, other.__class__.__name__
        print self._bag._items, other._bag._items
        return self._bag == other._bag
        
    def __repr__(self):
        return "{0}({1})".format(str(self.__class__.__name__), repr(self._order))
        
class OrderedBag(OrderedFrozenBag, collections.MutableSet):
    """
    Like a Bag, but iterating will keep the order things were put in. New items
    are added to the end of the OrderedBag - if you need anything else you can
    convert it to a tuple or list and make a new bag.
    
    Comparisons are still as for a Bag so OrderedBag([1,2,1]) == OrderedBag([2,1,1])
    will return True.    
    """
    
    def __init__(self, itterable):
        self._order = list(itterable)
        self._bag = Bag(self._order)
        
    def add(self, item):
        self._order.append(item)
        self._bag.add(item)
        
    def discard(self, item):
        self._order.remove(item)
        self._bag.discard(item)
        
        
    def __hash__(self):
        raise TypeError, "unhashable type: '{0}'".format(str(self.__class__.__name__))
