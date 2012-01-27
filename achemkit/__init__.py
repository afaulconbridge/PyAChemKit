"""
Detailed documentation for all the components of AChemKit.
It is generated directly from the source code, so should be up-to-date.
"""

# Import Psyco if available
try:
    import psyco
    psyco.full()
except ImportError:
    pass
   
__version__ = "0.4.0"
   
from achemkit.utils.bag import Bag, FrozenBag, OrderedBag, OrderedFrozenBag
from achemkit.reactionnet import ReactionNetwork
from achemkit.utils.simpledot import SimpleDot
from achemkit.reactionnetdot import net_to_dot
from achemkit.randomnet import Uniform
from achemkit.randomnet import Linear

from achemkit.bucket import Bucket, Event

from achemkit.achem import AChem, AChemReactionNetwork

from achemkit.sim.reactor import Reactor
from achemkit.sim.simple import sim_enumerate, sim_itterative, sim_stepwise, net_enumerate
from achemkit.sim.simple import ReactorEnumerate, ReactorItterative, ReactorStepwise
from achemkit.sim.gillespie import sim_gillespie, ReactorGillespieLike

import achemkit.properties
import achemkit.properties_wnx
import achemkit.utils.stat

from achemkit.utils.datafile import data_from_file, data_to_file
