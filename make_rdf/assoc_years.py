#!/usr/local/bin/python3

from rdflib import URIRef, Literal
from pathlib import Path
import pandas as pd
import rdflib
import mkrdfLib.tools as emg
import json
import re

from mkrdfLib.set_config import *
with open("named_entity_config.json", "r") as conf_file:
    ne_conf = json.load(conf_file)

datesg_name = ne_conf["rdf_source"]["dates"]
datesg_path = Path(rdf_output_hdir) / datesg_name

datesg = rdflib.Graph()

with open(datesg_path, "r") as infile:
    datesg.parse(source=infile, format=rdf_out_form)

fonds_df = pd.read_csv(fonds_csv_path)

def short_date(full_date):
    yearReg = re.compile(r'^([^\.]*\.\d\d)')
    short_date = yearReg.match(full_date)
    if short_date:
        return short_date.group(1)
    else:
        return "NN"

#dict {pnum: NormalizedYearVal}
pnumDate_dict =  dict(zip(
    fonds_df['id_text'].transform(lambda id: "P" + str(id).zfill(6)), 
    fonds_df['date_of_origin']
))

for pnum in pnumDate_dict:

    dateURI = datesg.value(
        predicate=RICO.normalizedDateValue, 
        object=Literal(short_date(str(pnumDate_dict[pnum])))
    )

    recURI = URIRef((id_root + "record/" + pnum))

    if dateURI:
        date_trip = (
            recURI,
            RICO.hasBeginningDate,
            dateURI         
        )
        g.add(date_trip)

    emg.write_g(rdf_output_hdir / f"recs-dates.{rdf_out_ext}", g, rdf_out_form)