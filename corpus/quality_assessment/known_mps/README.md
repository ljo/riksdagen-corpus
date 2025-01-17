README
======

In the file are ids and, names and iort for all mps during 1867-1993/94. It has been taken from registers of the two books:

Anders Norberg m. fl. Tvåkammarriksdagen 1867-1970. Ledamöter och valkretsar. Sveriges Riksdag och Almqvist & Wiksell, 1986

Norberg, Anders, and Björn Asker. Enkammarriksdagen: 1971-1993/94: ledamöter och valkretsar. Almqvist & Wiksell, 1996.

The csv-file consists of three columns: 
- wikidata_id: the wikidata id for the mp, 
- name: the name in the parliament (including iort), 
- source: the page, book number and book (Norberg et al, 1986, or Norberg and Asker, 1996)



 
## Known MPs
The catalog -- `catalog.csv` -- was compiled by Emil (@emla5688) and Magnus (@salgo60) using the  (Norberg et al, 1986, or Norberg and Asker, 1996) books and wikidata.

Bob (@BobBorges) cleaned the csv: strings containing commas (now a semi-colonsv file), aligned columns, filled in some missing info and split iort from the surname.

In theory, it contains all MPs for period (1867--1993/94).




### "missing_" files


These are generated by running the db unit test locally, with the `running_local` variable (line 16) set to True but not tracked in the repo. 



### "integrity-error_" files

These are results of locally run tests that check the integrity of catalog.csv

* wiki_id exists and is not "Q00FEL00"
* iort exists
* birth date exists

These are not tracked in the repo.



### "prioritized" wiki IDs

The `unique_missing_QIDs.json` file contains the list of wiki_ids that appear in each "missing_" file. In addition those "missing_" files in which the ID appears and ordered by N such "missing_" files. Thus, it's easy to prioritize "most absent" IDs by working from the top of the list, or by "missing_" type.. eg, all the IDs missing from `person.csv` first

Regenerate this file with `scripts/ls-missing-MP-QIDs.py`, which also prints info about duplicate QIDs and dummy QIDs (Q00FEL00).