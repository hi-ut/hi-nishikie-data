import shutil
import requests
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time
import hashlib

files = glob.glob("../../../docs/api/iiif/collection/*.json")

selections = []

curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://hi-ut.github.io/nishikie-data/api/iiif/curation/top.json",
    "@type": "cr:Curation",
    "label": "錦絵ギャラリー",
    "selections": selections
}

for i in range(len(files)):

    file = files[i]

    with open(file) as f:
        collection = json.load(f)

    if "manifests" not in collection:
        continue

    manifests = collection["manifests"]
    
    for j in range(len(manifests)):
        m = manifests[j]

        uri = m["@id"]

        thumbnail = ""
        id = hashlib.md5(uri.encode('utf-8')).hexdigest()

        if "thumbnail" in m:
            if "@id" in m["thumbnail"]:
                thumbnail = m["thumbnail"]["@id"]
            else:
                thumbnail = m["thumbnail"]
        
        if thumbnail == "":
            continue

        selections.append({
            "@id": id+"/range",
            "@type": "sc:Range",
            "members" : [
                { 
                    "label" : m["label"],
                    "metadata": m["metadata"],
                    "@id": uri,
                    "@type": "sc:Canvas",
                    "thumbnail": thumbnail
                } 
            ],
            "within": {
                "@id": uri,
                "@type": "sc:Manifest",
                "label": m["label"]
            }
        })

with open("../../../docs/api/iiif/curation/top.json", 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))