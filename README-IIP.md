
iip ingest: new places

This all happens in ~/Documents/files/P/pleiades-batching:

1. Exports:

 * first sheet (places) of spreadsheet to CSV as data/insc-israel-palestine/iip-places.csv
 * second sheet (alternate names) to CSV as data/insc-israel-palestine/iip-altnames.csv
 
 TBD: third sheet

2. Convert CSV to JSON:
    
    python convert.py data/insc-israel-palestine/iip-places.csv data/insc-israel-palestine/iip-places-xwalk.json data/insc-israel-palestine/iip-places.json

    python convert.py data/insc-israel-palestine/iip-altnames.csv data/insc-israel-palestine/iip-altnames-xwalk.json data/insc-israel-palestine/iip-altnames.json

3. Determine places that need to be created and prepare data for the update script:

    python massage-iip-places.py data/insc-israel-palestine/iip-places.json data/insc-israel-palestine/iip-places-ready.json

    NB: if there were altnames, be sure to include them with the -a option, like this:

    python massage-iip-places.py -a data/insc-israel-palestine/iip-altnames.json data/insc-israel-palestine/iip-places.json data/insc-israel-palestine/iip-places-ready.json

4. Run the update script to create places

    (this has to be done in the pleiades3-buildout folder)

    bin/instance run scripts/batch_update.py --create ~/Documents/files/P/pleiades-batching/data/insc-israel-palestine/iip-places-ready.json > ~/Documents/files/P/pleiades-batching/data/insc-israel-palestine/iip-places-results.txt

5. Manually check some of these places in the plone to make sure they got created (and reindexed) properly. A search for the tag will verify they were reindexed.

6. Save the output from the update script! This has the IDs you need in order to be able to upload the Locations and Names that should be inside these newly created places. Turn it into useful JSON as follows:

  python pairpids.py data/insc-israel-palestine/iip-places-results.txt data/insc-israel-palestine/iip-pid-pairs.json

7. Update the subordinates information that was originally created by the massage-iip-places.py script so that the PIDs assigned to the places we just created are used as the parent context for the names and locations we are about to create.

  python massage-iip-subordinates.py data/insc-israel-palestine/iip-places-ready.json data/insc-israel-palestine/iip-pid-pairs.json data/insc-israel-palestine/iip-subordinates-ready.json

8. Run the batch update script again, this time to create the subordinate names and locations.

  bin/instance run scripts/batch_update.py --create ~/Documents/files/P/pleiades-batching/data/insc-israel-palestine/iip-subordinates-ready.json

  


