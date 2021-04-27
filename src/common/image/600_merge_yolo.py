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

dir = "../../../docs/api/iiif/curation"

path = dir + "/top_text.json"

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    idMap = {}

    for selection in selections:
        members = selection["members"]

        for member in members:

            uri = member["@id"]
            id = hashlib.md5(uri.encode('utf-8')).hexdigest()

            print(id)

            path = "yolo/data/"+id+".json"

            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)

                members2 = data["selections"][0]["members"]

                arr = []

                for member2 in members2:
                    metadata = member2["metadata"]

                    for m in metadata:
                        if m["label"] == "Tag":
                            value = m["value"]

                            if value not in arr:
                                arr.append(value)

                if len(arr) > 0:
                    member["metadata"].append({
                        "label" : "機械タグ",
                        "value" : arr
                    })

    '''
    for selection in selections:
        members = selection["members"]

        for member in members:

            thumbnail = member["thumbnail"]

            uri = member["@id"]

            print(uri)
            id = hashlib.md5(uri.encode('utf-8')).hexdigest()

            path = "data/json/similar_images/"+id+".json"

            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)

                images = []
                max = 20
                if len(data) < max:
                    max = len(data)
                for i in range(0, max):
                    tid = data[i]
                    if tid in idMap:
                        images.append(idMap[tid])
                member["images"] = images
    '''

filename = "/top_yolo.json"
with open(dir + filename, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))