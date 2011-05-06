"""
A collection of classes providing containers. These use the abstract
base classes (ABCs) from :py:mod:`collections` module to satisfy 
isinstance() criteria for API provision. 
"""

import collections
import itertools

class FrozenBag(collections.Set):
    """
    A Bag is like a set, but can contain duplicates.
    
    Also, a Bag is like a list, but is always ordered.
    
    Note: objects must be both hashable and sortable. By default, 
    python objects are sorted by id(), but this is not consistent.
    As there is no easy way to test this, if you get wierd results
    this may be the cause.
    """    
    __slots__ = ["_items"]
        
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed ("+repr(iterable)+")"
        self._items = tuple(sorted(iterable))
                
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
        
    def count(self, item):
        return self._items.count(item)
        
    def __getstate__(self):
        return self._items
        
    def __setstate__(self, state):
        self._items = state
        
    def __eq__(self, other):
        if other is None:
            return False
        if other.__class__ is not self.__class__:
            return False
        if len(self) != len(other):
            return False
        for a,b in itertools.izip(self, other):
            if a != b:
                return False
        return True
    
    
class Bag(FrozenBag, collections.MutableSet):
    """
    A Bag is like a set, but can contain duplicates.
    
    Also, a Bag is like a list, but is always ordered.
    """
    __slots__ = ["_items"]
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed ("+repr(iterable)+")"
        self._items = sorted(list(iterable))
        
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
    __slots__ = ["_items", "_order", "_bag"]
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed ("+repr(iterable)+")"
        elif not isinstance(iterable, tuple):
            iterable = tuple(iterable)
        self._order = iterable
        for item in self._order:
            if not isinstance(item, collections.Hashable):
                raise TypeError, "non-hashable passed ("+repr(item)+")"
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
        if other is None:
            return False
        elif self.__class__ is other.__class__:
            return self._bag == other._bag
        else:
            raise ValueError, "Comparison with different class ("+other.__class__.__name__+")"
            return False
        
    def __lt__(self, other):
        if other.__class__ != self.__class__:
            raise TypeError
        return self._bag < other
        
    def __repr__(self):
        return "{0}({1})".format(str(self.__class__.__name__), repr(self._order))
        
    def count(self, item):
        return self._order.count(item)
        
    def index(self, item):
        return self._order.index(item)
        
    def __getitem__(self, index):
        return self._order[index]
        
    def __getstate__(self):
        return (self._bag, self._order)
        
    def __setstate__(self, state):
        self._bag = state[0]
        self._order = state[1]
        
class OrderedBag(OrderedFrozenBag, collections.MutableSet):
    """
    Like a Bag, but iterating will keep the order things were put in. New items
    are added to the end of the OrderedBag - if you need anything else you can
    convert it to a tuple or list and make a new bag.
    
    Comparisons are still as for a Bag so OrderedBag([1,2,1]) == OrderedBag([2,1,1])
    will return True.    
    """
    __slots__ = ["_items", "_order", "_bag"]
        
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed ("+repr(iterable)+")"
        self._order = list(iterable)
        self._bag = Bag(self._order)
        
    def add(self, item):
        self._order.append(item)
        self._bag.add(item)
        
    def discard(self, item):
        self._order.remove(item)
        self._bag.discard(item)
        
    def __hash__(self):
        raise TypeError, "unhashable type: '{0}'".format(str(self.__class__.__name__))
        
        
class OrderedFrozenBagCache(object):
    cache = {}
    def __new__(cls, iterable):
        if not isinstance(iterable, tuple):
            iterable = tuple(iterable)
        if iterable not in cls.cache:
            cls.cache[iterable] = OrderedFrozenBag(iterable)
        return cls.cache[iterable]
