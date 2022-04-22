from pathlib import Path
from rdflib import Graph

def write_g(file_path:Path, gvar:Graph, varFormat:str='json-ld'):
    if not file_path.parent.exists():
        file_path.parent.mkdir()
    with open(file_path, 'w') as outfile:
        outfile.write(gvar.serialize(format=varFormat))