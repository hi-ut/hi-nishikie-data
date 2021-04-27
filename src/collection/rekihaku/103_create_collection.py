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

dirname = "rekihaku"

prefix0 = "https://hi-nishikie.web.app"
static_dir = "../../../static"

files = glob.glob(static_dir+"/api/iiif/{}/*/manifest.json".format(dirname))

manifests = []

for file in files:
    print(file)

    json_open = open(file, 'r')
    df = json.load(json_open)

    manifests.append({
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": df["@id"],
        "license": df["license"],
        "metadata" : df["metadata"],
        "@type": "sc:Manifest",
        "label" : df["label"],
        "thumbnail": df["thumbnail"]
    })

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix0 + "/api/iiif/collection/{}.json".format(dirname),
    "@type": "sc:Collection",
    "manifests": manifests,
    "label": "歴博・館蔵錦絵コレクション",
    "vhint": "use-thumb"
}

f_path = collection["@id"].replace(prefix0, static_dir)
dirname = os.path.dirname(f_path)
os.makedirs(dirname, exist_ok=True)

with open(f_path, 'w') as outfile:
    json.dump(collection, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))