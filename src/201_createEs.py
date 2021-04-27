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

static_dir = "../static"

files = glob.glob(static_dir + "/api/iiif/collection/*.json")

actions = []

for file in files:
    if "top.json" in file:
        continue

    json_open = open(file, 'r')
    df = json.load(json_open)

    manifests = df["manifests"]

    for m in manifests:

        

        id = "-1"
        source = ""

        if "rekihaku" in file:
            id = "rekihaku-" + m["@id"].split("/")[-2]
            source = "国立歴史民俗博物館"
        else:
            id = "hi-" + m["@id"].split("/")[-2]
            source = "東京大学史料編纂所"

        title = m["label"]

        obj = {
            "_label": [title],
            "_url" : ["https://hi-nishikie.web.app/item/"+id],
            "_thumbnail" : [m["thumbnail"]["@id"]],
            "source" : [source],
            "_manifest" : [m["@id"]]
        }

        metadata = m["metadata"]

        description = []

        fulltext = [title]

        for m2 in metadata:
            label = m2["label"]
            value = m2["value"]

            # obj[label] = [value]

            if value:
                description.append(label+": " + value)
                fulltext.append(value)

        obj["fulltext"] = [", ".join(fulltext)]
        obj["description"] = description

        actions.append({
            "_index": "main",
            "_id": id,
            "_source" : obj
        })

with open("data/es.json", 'w') as outfile:
    json.dump(actions, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))