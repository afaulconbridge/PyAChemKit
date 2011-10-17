import collections

import umpf

from achemkit import OrderedFrozenBag
    
class Reactor(object):
    def __init__(self, achem, mols, *args, **kwargs):
        self.achem = achem
        self.mols = mols
            
    def do(self):
        raise NotImplementedError, "Reactor is an abstract class"
    
    def to_disk(self, filename):
        pickle.dump(self, open(filename, "w+b"), 2)
        
    def to_disk_gz(self, filename):
        pickle.dump(self, gzip.GzipFile(filename+".gz", "w+b"), 2)
        
    @staticmethod
    def from_disk(filename):
        return pickle.load(open(filename, "r+b"))
            
    @staticmethod
    def from_disk_gz(filename):
        return pickle.load(gzip.GzipFile(filename+".gz", "r+b"))
    
