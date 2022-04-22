#!/usr/local/bin/python3

import pandas as pd
import json

full_cat_df = pd.read_csv("../cdli_data/cdli_cat.csv")

with open("../first_info_gen/search_config.json", "r") as infile:
    searches = json.load(infile)

def intersect_dflist(dflist):
    df_out = dflist[0]
    for df in dflist[1:]:
        df_out = pd.merge(df_out, df)
    return df_out

def combine_terms(col_name, term_list, df=full_cat_df):
    term_list_len = len(term_list)
    df_out = df[df[col_name].str.startswith(term_list[0], na=False)]
    if term_list_len > 1:
        for term in term_list[1:]:
            df_out = pd.merge(
                df_out, 
                df[df[col_name].str.startswith(term, na=False)],
                how="outer"
            )

    return df_out

def combine_categories(search_dict):
    return intersect_dflist([
        combine_terms(cat, search_dict[cat])
        for cat in search_dict
    ])

search_keys = [k for k in searches]

fonds_df = combine_categories(searches[search_keys[0]])
if len(search_keys) > 1:
    for search in search_keys[1:]:
        fonds_df = pd.merge(
            fonds_df, 
            combine_categories(searches[search]), 
            how="outer"
        )

fonds_df.to_csv("../fonds_info/fonds_cat.csv", index=False)

print(
    f"Combined total {len(fonds_df)}"
)

pnums = [
    "P" + str(pnum).zfill(6)
    for pnum in
    fonds_df["id_text"]
    ]

with open("../fonds_info/fonds_pnums.txt", "w") as of:
    for pnum in pnums:
        of.write(pnum + "\n")