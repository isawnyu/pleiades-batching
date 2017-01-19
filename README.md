# Support for Pleiades batch updates

## Reporting Bugs and Requesting New Features

**Please open bug reports and feature requests on [the central *Pleiades* Gazetteer issue tracker](https://github.com/isawnyu/pleiades-gazetteer/issues).**

## What This Is (and Isn't)

The code and documentation in this repository are intended to support the creation, submission, and validation of data intended for behind-the-scenes "batch" input into the [*Pleiades* gazetteer of ancient places](https://pleiades.stoa.org) (both updates to existing content and creation of new content). 

This repository **does not** contain the actual script used to perform the batch update to the *Pleiades* Plone instance. That can be found in [the main *Pleiades* buildout repository](https://github.com/isawnyu/pleiades3-buildout), "jazkarta-plone4" branch, as [scripts/batch_update.py](https://github.com/isawnyu/pleiades3-buildout/tree/jazkarta-plone4/scripts). 

## How?!

## Modules and Scripts in this Repository

### csv_splitter.py

A script for splitting CSV field values containing comma-delimited lists.

### names.py

### massage-names.py

### pair_pids.py

### vocab_getter.py

### Utility Modules

 - arglogger.py
 - vocabularies.py
 - csv_utilities.py
 - normalize_space.py

## Todo

 - Refactor as a standard Python package, rather than a script pile.
 - Write packaging script for massage-*.py script outputs.

## Deprecated Stuff in This Module

### convert.py

An early attempt at converting CSV into JSON suitable for the Pleiades batch loading script. It is partly superseded by the massage-*.py family of scripts, but we will also need to write a packaging script that will take output from the massage-*.py scripts and turn them into the JSON that the batch upload script expects.


