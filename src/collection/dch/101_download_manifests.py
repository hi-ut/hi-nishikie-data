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


files = glob.glob("data/*.json")

for file in files:

    with open(file) as f:
        obj = json.load(f)

    manifests = obj["manifests"]

    for i in range(len(manifests)):

        m = manifests[i]

        print(i+1, len(manifests))

        manifest = m["@id"]

        uuid = manifest.split("/")[-2]

        path = "manifests/{}.json".format(uuid)

        try:
            df = requests.get(manifest,verify=False).json()
            with open(path, 'w') as outfile:
                json.dump(df, outfile, ensure_ascii=False,
                            indent=4, sort_keys=True, separators=(',', ': '))

        except Exception as e:
            print(e)