# Support for Pleiades batch updates

## Reporting Bugs and Requesting New Features

**Please open bug reports and feature requests on [the central *Pleiades* Gazetteer issue tracker](https://github.com/isawnyu/pleiades-gazetteer/issues).**

## What This Is (and Isn't)

The code and documentation in this repository are intended to support the creation, submission, and validation of data intended for behind-the-scenes "batch" input into the [*Pleiades* gazetteer of ancient places](https://pleiades.stoa.org) (both updates to existing content and creation of new content). 

This repository **does not** contain the actual script used to perform the batch update to the *Pleiades* Plone instance. That can be found in [the main *Pleiades* buildout repository](https://github.com/isawnyu/pleiades3-buildout), "jazkarta-plone4" branch, as [scripts/batch_update.py](https://github.com/isawnyu/pleiades3-buildout/tree/jazkarta-plone4/scripts). 

## How?!

 1. Prepare data in a series of CSV files in accordance with guidance herein (todo).
 2. Run appropriate "massage" scripts on the provided CSV files to validate their content and, where appropriate, to enhance it.
 3. Run packaging script (todo) on the output(s) of the "massage" scripts to get them ready for the "batch_update" script.
 4. Fire up a test instance of Pleiades and test-run the batch_update script with the new content.
 5. Run the new content through the batch update script on the production Pleiades site.

## Versions, Formats, Encodings, and Other Gotchas

This code is tested with Python 3.6.0, running on Apple OSX El Capitan (10.11.6). Python 2.x is **not supported**.

Supported file formats include CSV and JSON (but see "todo" section, below). Unless a different encoding is specified, all scripts and functions in this package assume the text in such files is UTF-8-encoded without a BOM. That's a requirement for valid JSON, but an assumption for CSV. 

Caveat utilitor: older versions of Microsoft Excel do not support any character encoding other than ASCII (thus irrevocably borking your placenames!), and recent versions' "Save as UTF-8 CSV" functionality silently adds a BOM. So, don't use old versions of Excel to prepare content for pleiades-batching, and be sure to pass "utf-8-sig" instead of "utf-8" as the encoding for scripts and functions defined herein.

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

Defines vocabularies used in pleiades-batching tools.

### csv_utilities.py

Reusable code for working with CSV files.

### normalize_space.py

Function to normalize whitespace in a string.

## Todo

 - Refactor as a standard Python package, rather than a script pile.
 - Write packaging script for "massage" script outputs.
 - Add JSON input support.
 - Provide guidance on CSV format and contents.

## Deprecated Stuff in This Module

### convert.py

An early attempt at converting CSV into JSON suitable for the Pleiades batch loading script. It is partly superseded by the "massage" family of scripts, but we will also need to write a packaging script that will take output from the "massage" scripts and turn them into the JSON that the batch upload script expects.

### pair_pids.py

The docstring says: "match up placenames and pids from update script output" but what actual good is it now?


