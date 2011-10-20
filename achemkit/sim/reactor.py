"""
This module contains an abstraction of reaction vessels for use as
the mixing algorithm component of an Artificial Chemistry.

Rather than using this directly, subclasses should be created that implement
:py:func:`Reactor.do` in a specific way. See 
:py:class:`achemkit.ReactorEnumerate`, :py:class:`achemkit.ReactorItterate`, 
and :py:class:`achemkit.ReactorStepwise` for examples.
"""

import collections

import umpf

from achemkit import OrderedFrozenBag
    
class Reactor(object):
    """
    Abstract class that defines common features useful for mixing algorithms.
    """
    def __init__(self, achem, mols):
        """
        :param achem: py:class:`achemkit.achem.AChem` object or equivalent.
        :param mols: Initial molecules
        """
        self.achem = achem
        self.mols = mols
            
    def do(self):
        """
        This is an abstract method that must be implemented by subclassess. May
        take parameters as needed.
        """
        raise NotImplementedError, "Reactor is an abstract class"
    
    def to_disk(self, filename):
        """
        Store this object to disk as serialized by :py:mod:`pickle`.
        
        :param filename: Name of file to write to.
        """
        pickle.dump(self, open(filename, "w+b"), 2)
        
    def to_disk_gz(self, filename):
        """
        Store this object to disk as serialized by :py:mod:`pickle` and 
        compressed by :py:mod:`gzip`.
        
        :param filename: Name of file to write to.
        """
        pickle.dump(self, gzip.GzipFile(filename+".gz", "w+b"), 2)
        
    @staticmethod
    def from_disk(filename):
        """
        Load a Reactor from disk that has be previously stored by 
        :py:meth:`to_disk`
        
        :param filename: Path to read from.
        """
        return pickle.load(open(filename, "r+b"))
            
    @staticmethod
    def from_disk_gz(filename):
        """
        Load a Reactor from disk that has be previously stored by 
        :py:meth:`to_disk_gz`
        
        :param filename: Path to read from.
        """
        return pickle.load(gzip.GzipFile(filename+".gz", "r+b"))
    
