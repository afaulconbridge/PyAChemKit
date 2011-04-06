"""
A collection of classes providing containers. These use the abstract
base classes (ABCs) from :py:mod:`collections` module to satisfy 
isinstance() criteria for API provision. 
"""

import collections

class FrozenBag(collections.Set):
    """
    A Bag is like a set, but can contain duplicates.
    
    Also, a Bag is like a list, but is always ordered.
    """
    _items = ()
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed"
        self._items = tuple(sorted(list(iterable)))
        for item in self._items:
            if not isinstance(item, collections.Hashable):
                raise TypeError, "non-hashable passed"
        
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
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed"
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
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed"
        self._order = tuple(iterable)
        self._bag = FrozenBag(self._order)
        for item in self._order:
            if not isinstance(item, collections.Hashable):
                raise TypeError, "non-hashable passed"
        
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
        if other.__class__ == self.__class__:
            return self._bag == other._bag
        else:
            for a,b in zip(self, other):
                if a != b:
                    return False
            return True
        
    def __lt__(self, other):
        if other.__class__ != self.__class__:
            raise TypeError
        return self._bag < other
        
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
    
    def __init__(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise TypeError, "non-iterabble passed"
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

