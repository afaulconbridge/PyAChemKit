############
File Formats
############

AChemKit uses a number of text file formats for data storage and as intermediates between various components.


.. _chem_file_format:

`.chem` Format
==============

The `.chem` format is used to abstractly describe a chemistry in terms of reactions. Each reaction is represented as a single line, separated into reactants and products by the symbol `->`. Blank lines and lines starting with `#` are ignored - this is useful to remove reactions temporarily or to add documentation. Additional white-space within a line is also ignored. 

Reactants and/or products can contain multiple molecular species, separated by `+`. No explicit restrictions are placed on the names of molecular species, but it is recommended to be restricted to alpha-numeric characters (upper-case and lower-case) as well as `()` and `[]`. In particular, the following should be avoided: `+`, `-`, `>`. At this time, escaping or quoting is not supported.

The reactant/product separator `->` is also used to represent the rate constant of the reaction, if specified. This is done by a floating-point number between the `-` and `>` characters. For example, `-2.0>` represents a reaction with a rate constant of 2.0. Integers can also be used, but will be converted to floating-point, e.g. `-2>` is a rate constant of 2.0. If a rate constant is not specified, it defaults to 1.0. Rate constants <=0.0 are not valid, and in some situations rate constants >1.0 may not be either.

It is not valid to have more than one reaction with the same combination of reactants and products - in any order and with any rate. For example, `A + B -> C` cannot appear in the same file as `B + A -2.0> C`.

It is not valid to have the same molecular species in both reactants and products. For example `A + B -> B + A` is not valid.

Either the reactants or products can be omitted from a reaction, e.g. `A ->`. This corresponds to material being added or removed from the system.

When a `.chem` file is generated, reactants and products of all reactions are sorted by their string representations, and then reactions are sorted before being output. 

Below is a valid example `.chem` file:

.. include:: ../AChemKit/tests/sampleA.chem
   :literal:

