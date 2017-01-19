# Support for Pleiades batch updates

## Reporting Bugs and Requesting New Features

**Please open bug reports and feature requests on [the central *Pleiades* Gazetteer issue tracker](https://github.com/isawnyu/pleiades-gazetteer/issues).**

## What This Is (and Isn't)

The code and documentation in this repository are intended to support the creation, submission, and validation of data intended for behind-the-scenes "batch" input into the [*Pleiades* gazetteer of ancient places](https://pleiades.stoa.org) (both updates to existing content and creation of new content). 

This repository **does not** contain the actual script used to perform the batch update to the *Pleiades* Plone instance. That can be found in [the main *Pleiades* buildout repository](https://github.com/isawnyu/pleiades3-buildout), "jazkarta-plone4" branch, as [scripts/batch_update.py](https://github.com/isawnyu/pleiades3-buildout/tree/jazkarta-plone4/scripts). 

## How?!

## Modules and Scripts in this Repository

NB: Usage for scripts can be displayed with the "-h" option, like:

```
python massage-names.py -h
```

### csv_splitter.py

A script for splitting CSV field values containing comma-delimited lists.

### names.py

Construct and validate data for *Pleiades* name resources.

Defines the class ```PleiadesName```, whose attributes and methods constitute the full capabilities of this module.

Nosetests in tests/test_names.py. 

### massage-names.py

Script to validate and augment *Pleiades* names data for batch upload create.

### Utility Modules

### arglogger.py

Defines a Decorator to log argument calls to functions.

### vocab_getter.py

Script to scrape HTML version of a Pleiades vocab page and save as plain text.

### vocabularies.py

### csv_utilities.py

### normalize_space.py

## Todo

 - Refactor as a standard Python package, rather than a script pile.
 - Write packaging script for "massage" script outputs.

## Deprecated Stuff in This Module

### convert.py

An early attempt at converting CSV into JSON suitable for the Pleiades batch loading script. It is partly superseded by the "massage" family of scripts, but we will also need to write a packaging script that will take output from the "massage" scripts and turn them into the JSON that the batch upload script expects.

### pair_pids.py

The docstring says: "match up placenames and pids from update script output" but what actual good is it now?


