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

files = glob.glob("data/*.html")

for file in files:
    print(file)
    soup = bs4.BeautifulSoup(open(file), 'lxml')
    aas = soup.find_all("a")

    for a in aas:
        # print(a)
        manifest = a.get("href")
        if manifest and "manifest" in manifest:

            uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

            path = "manifests/{}.json".format(uuid)

            if os.path.exists(path):
                continue

            #########

            time.sleep(0.5)

            print(manifest)
            
            try:
                df = requests.get(manifest,verify=False).json()
                with open(path, 'w') as outfile:
                    json.dump(df, outfile, ensure_ascii=False,
                                indent=4, sort_keys=True, separators=(',', ': '))

            except Exception as e:
                print(e)
