#!/usr/local/bin/python3

"""
Uses the csv slice made in first_info_gen/delimit_fonds.py
to generate triplets for each document/line:
    <PNUM>, rdf:type, rico:Record
            rico:isOrWasIncludedIn, <fonds>
            emont:identCDLI, "id_text"
            emont:identColl, "museum_no"
            emont:identPub "primary_publication"
            rico:hasInstantiation, <PNUM#in1>
    <PNUM#in1>, rdf:type, rico:Instantiation
                rico:hasOrHadLocation, "collection"
                rico:hasCarrierType, "material"
                rico:hasCarrierType, "object_type"
                rico:hasExtent, _:BNode
    _:Bnode,    rdf:type, rico:CarrierExtent
                rico:height, "height"
                rico:width, "width
                rico:unitOfMeasurement, "cm"
TODO:   add functionality to deal w/ multiple instantiations,
        check an existing graph to avoid creating redundant bnodes
"""

# import datetime
from rdflib import URIRef, RDF, Literal, BNode
import pandas as pd
import mkrdfLib.tools as emg
from mkrdfLib.set_config import *

fondsdf = pd.read_csv(fonds_csv_path)

# output_hdir = Path(config["rdf_output_hdir"])
    
rows = fondsdf['id_text']
print(f'{len(rows)} documents to process')

for row in rows:
    rowinfo = fondsdf.loc[fondsdf['id_text'] == row]
    pnum = 'P' + str(row).zfill(6)
    pnumUri = URIRef((id_root + 'record/'+ pnum))
    instUri = pnumUri + '#in1'
    
    g.add((pnumUri, RDF.type, RICO.Record))
    g.add((pnumUri, RICO.isOrWasIncludedIn, fondsURI))

    #Triplets about id numbers
    g.add((pnumUri, EMONT.identCDLI, Literal(pnum)))
    if rowinfo['museum_no'].notna().all():
        g.add((
            pnumUri, 
            EMONT.identColl, 
            Literal(rowinfo['museum_no'].iloc[0])
        ))
    if rowinfo['primary_publication'].notna().all():
        g.add((
            pnumUri, 
            EMONT.identPub, 
            Literal(rowinfo['primary_publication'].iloc[0])
        ))
    
    #Triplets about physical instantiation
    g.add((pnumUri, RICO.hasInstantiation, instUri))
    g.add((instUri, RDF.type, RICO.Instantiation))
    if rowinfo['collection'].notna().all():
        g.add((
            instUri, 
            RICO.hasOrHadLocation, 
            Literal(rowinfo['collection'].iloc[0], lang="en")
        ))
    if rowinfo['material'].notna().all():
        g.add((
            instUri, 
            RICO.hasCarrierType, 
            Literal(rowinfo['material'].iloc[0], lang="en")
        ))
    if rowinfo['object_type'].notna().all():
        g.add((
            instUri, 
            RICO.hasCarrierType, 
            Literal(rowinfo['object_type'].iloc[0], lang="en")
        ))
    
    #Triplets about physical extent
    if (rowinfo['height'].iloc[0] or rowinfo['width'].iloc[0]) != ('?' or ''):
        if (type(rowinfo['height'].iloc[0]) or type(rowinfo['width'].iloc[0])) != float:
            extNode = BNode()
            g.add((instUri, RICO.hasExtent, extNode))
            g.add((extNode, RDF.type, RICO.CarrierExtent))
            if rowinfo['height'].iloc[0] != ('?' or '') and type(rowinfo['height'].iloc[0]) != float:
                g.add((extNode, RICO.height, Literal(rowinfo['height'].iloc[0])))
            if rowinfo['width'].iloc[0] != ('?' or '') and type(rowinfo['width'].iloc[0]) != float:
                g.add((extNode, RICO.width, Literal(rowinfo['width'].iloc[0])))
            g.add((extNode, RICO.unitOfMeasurement, Literal('cm')))


# now = datetime.datetime.now()
# timestamp = str(now.strftime("%Y_%m_%d_(%H_%M)"))

emg.write_g(rdf_output_hdir / "cdlidb_data.jsonld", g)