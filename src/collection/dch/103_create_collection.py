import sys
import bs4
import hashlib
import json
import bs4
import requests
import time
import os
import urllib.parse
import csv
import glob
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import pandas as pd
import uuid
import bs4
import hashlib

dirname = "dch"
label = "Digital Cultural Heritage"

prefix0 = "https://hi-ut.github.io/nishikie-data"
static_dir = "../../../docs"

files = glob.glob("manifests/*.json")

manifests = []

for file in files:
    print(file)

    json_open = open(file, 'r')
    df = json.load(json_open)

    if "thumbnail" not in df:
        continue

    m = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": df["@id"],
        "metadata" : df["metadata"],
        "@type": "sc:Manifest",
        "label" : df["label"],
        "thumbnail": df["thumbnail"]
    }

    if "license" in df:
        m["license"] = df["license"]

    manifests.append(m)

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix0 + "/api/iiif/collection/{}.json".format(dirname),
    "@type": "sc:Collection",
    "manifests": manifests,
    "label": label,
    "vhint": "use-thumb"
}

f_path = collection["@id"].replace(prefix0, static_dir)
dirname = os.path.dirname(f_path)
os.makedirs(dirname, exist_ok=True)

with open(f_path, 'w') as outfile:
    json.dump(collection, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))