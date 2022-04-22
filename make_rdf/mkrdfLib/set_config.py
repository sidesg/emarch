#!/usr/local/bin/python3

import json
from rdflib import URIRef, Graph, Namespace
from pathlib import Path


with open("make_rdf_config.json", "r") as infile:
    gen_config = json.load(infile)

g = Graph()
uri_root =  gen_config["uri_root"]
id_root = uri_root + gen_config["id_stem"]

RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
EMONT = Namespace(id_root + "ontology#")
EMARCH = Namespace(uri_root)

fonds_uri_name = gen_config["fonds_uri_name"]
fondsURI = URIRef((uri_root + "record/" + fonds_uri_name))

fonds_csv_path = Path(gen_config["fonds_csv_path"])

rdf_output_hdir = Path(gen_config["rdf_output_hdir"])
    