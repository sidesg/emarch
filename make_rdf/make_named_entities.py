#!/usr/local/bin/python3

from rdflib import SKOS, URIRef, RDF, Literal, BNode
from pathlib import Path
import pandas as pd
import mkrdfLib.tools as emg
import json

from mkrdfLib.set_config import *

with open("named_entity_config.json", "r") as infile:
    ne_config = json.load(infile)

ne_source_dir = Path(ne_config["source_dir"])

def choose_import():
    choice = input(
        "What do you want to convert to RDF?\n"
        "1. Agents\n"
        "2. Dates\n"
        "3. Positions\n"
        "[Q]uit\n"
    )

    if choice == str(1):
        print("Feature coming soon!")

    if choice == str(2):
        import_dates()
        emg.write_g(rdf_output_hdir / "dates.jsonld", g)
        exit()
    
    if choice == str(3):
        import_pos()
        emg.write_g(rdf_output_hdir / "positions.jsonld", g)
        exit()

    if choice.lower().startswith("q"):
        exit()

    else:
        choose_import()


def import_pos():
    source_pth = ne_source_dir / ne_config["positions_filename"]
    positions_df = pd.read_csv(source_pth)

    positions = positions_df["id"]
    for pos_id in positions:
        rowinfo = positions_df.loc[positions_df['id'] == pos_id]
        posURI = URIRef((id_root + "position/" + pos_id))
        nameURI = posURI + "#n1"
        spelling = BNode()


        g.add((
            posURI,
            RDF.type,
            RICO.Position
        ))
        g.add((
            posURI,
            RICO.hasOrHadName,
            nameURI
        ))

        if rowinfo['belong'].notna().all():
            g.add((
                posURI,
                RICO.existsOrExistedIn,
                URIRef((uri_root + rowinfo['belong'].iloc[0]))
            ))

        if rowinfo['descr.'].notna().all():
            g.add((
                posURI,
                RICO.descriptiveNote,
                Literal(rowinfo['descr.'].iloc[0], lang="en")
            ))

        g.add((
            nameURI,
            RDF.type,
            EMONT.PrefName
        ))
        g.add((
            nameURI,
            RICO.normalizedValue,
            Literal(rowinfo['n1_normVal'].iloc[0])
        ))
        g.add((
            nameURI,
            EMONT.hasSpelling,
            spelling
        ))

        g.add((
            spelling,
            RDF.type,
            EMONT.Spelling
        ))
        g.add((
            spelling,
            SKOS.prefLabel,
            Literal(rowinfo['n1_s1_normVal'].iloc[0])
        ))
        
def import_dates():
    source_pth = ne_source_dir / ne_config["dates_filename"]
    ne_df = pd.read_csv(source_pth)

    positions = ne_df["id"]
    for pos_id in positions:
        rowinfo = ne_df.loc[ne_df['id'] == pos_id]
        idURI = URIRef((id_root + "date/" + pos_id))
        typeURI = URIRef((rowinfo['type'].iloc[0]))

        g.add((
            idURI,
            RDF.type,
            typeURI
        ))

        g.add((
            idURI,
            RICO.normalizedDateValue,
            Literal(rowinfo['normalizedDateValue'].iloc[0])
        ))
        g.add((
            idURI,
            RICO.expressedDate,
            Literal(rowinfo['expressedDate'].iloc[0], lang="en")
        ))

        if rowinfo['precedesInTime'].notna().all():
            g.add((
                idURI,
                RICO.precedesInTime,
                URIRef((id_root + "date/" + rowinfo['precedesInTime'].iloc[0]))
            ))       

        if rowinfo['isOrWasPartOf'].notna().all():
            g.add((
                idURI,
                RICO.isOrWasPartOf,
                URIRef((id_root + "date/" + rowinfo['isOrWasPartOf'].iloc[0]))
            )) 
        
        if rowinfo['ruler'].notna().all():
            g.add((
                idURI,
                RICO.isRelatedTo,
                URIRef((id_root + "agent/" + rowinfo['ruler'].iloc[0]))
            ))                  



choose_import()