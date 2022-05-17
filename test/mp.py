import unittest

import pandas as pd
from lxml import etree
from pyriksdagen.utils import validate_xml_schema, infer_metadata
from pyriksdagen.download import get_blocks
from pyriksdagen.export import create_tei, create_parlaclarin
from pyriksdagen.db import load_patterns, filter_db, load_ministers, load_metadata
from pathlib import Path
import progressbar

class Test(unittest.TestCase):

    # Official example parla-clarin 
    def test_protocol(self):
        parser = etree.XMLParser(remove_blank_text=True)

        def test_one_protocol(root, mp_ids, mp_db):
            mp_doa = mp_db[['id', 'born', 'dead']].drop_duplicates().reset_index(drop=True)

            found = True
            years = []
            date = None
            for docDate in root.findall(".//{http://www.tei-c.org/ns/1.0}docDate"):
                docDateYear = docDate.attrib.get("when", "unknown")
                date = docDateYear
                docDateYear = int(docDateYear.split("-")[0])
                years.append(docDateYear)

            for year in years:
                if year not in mp_ids:
                    year_db = filter_db(mp_db, year=year)
                    ids = list(year_db["id"])
                    mp_ids[year] = ids

            false_whos = []
            dead_whos = []
            unborn_whos = []
            for body in root.findall(".//{http://www.tei-c.org/ns/1.0}body"):
                for div in body.findall("{http://www.tei-c.org/ns/1.0}div"):
                    for ix, elem in enumerate(div):
                        if elem.tag == "{http://www.tei-c.org/ns/1.0}u":
                            who = elem.attrib.get("who", "unknown")
                            if who != "unknown":
                                born, dead = mp_doa.loc[mp_doa['id'] == who, ['born', 'dead']].iloc[0]

                                if not pd.isna(born):
                                    if min(years) < int(born[:4]) + 15:
                                        unborn_whos.append(who)

                                if not pd.isna(dead):
                                    if max(years) > int(dead[:4]):
                                        dead_whos.append(who)

                                elem_found = False
                                for year in years:
                                    if who in mp_ids[year]:
                                        elem_found = True

                                if not elem_found:
                                    found = False
                                    false_whos.append(who)

            return found, false_whos, dead_whos, unborn_whos

        # new
        folder = "corpus/protocols"
        _, mp_db, minister_db, speaker_db = load_metadata()
        mp_db = pd.concat([mp_db, minister_db, speaker_db])

        mp_ids = {}

        failed_protocols = []
        for outfolder in progressbar.progressbar(list(Path(folder).glob("*/"))):
            for protocol_path in outfolder.glob("*.xml"):
                protocol_id = protocol_path.stem
                path_str = str(protocol_path.resolve())
                root = etree.parse(path_str, parser).getroot()
                found, false_whos, dead_whos, unborn_whos = test_one_protocol(root, mp_ids, mp_db)
                if not found:
                    failed_protocols.append(protocol_id + " (" + false_whos[0] + ")")

        print("Protocols with inactive MPs tagged as speakers:", ", ".join(failed_protocols))
        print("Dead MPs tagged as speakers:", ", ".join(dead_whos))
        print("Children MPs tagged as speakers:", ", ".join(unborn_whos))

        self.assertEqual(len(failed_protocols), 0)




if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
