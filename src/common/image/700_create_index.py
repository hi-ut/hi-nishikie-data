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

path = dir + "/top_yolo.json"

results = []

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    

    for selection in selections:
        members = selection["members"]

        for member in members:

            uri = member["@id"]

            id = hashlib.md5(uri.encode('utf-8')).hexdigest()

            item = {
                "objectID" : id
            }

            metadata = member["metadata"]

            map = {}

            fulltext = []

            for m in metadata:
                label = m["label"]
                value = m["value"]

                field = "description"

                if field not in map:
                    map[field] = []

                if type(value) is str:
                    value = [value]

                if not value:
                    continue

                if label == "機械タグ":
                    map[label] = []

                

                for v in value:

                    if label == "機械タグ" and v not in map[label]:
                        map[label].append(v)

                    else:

                        v2 = label + ": " + v

                        if "http" in v2:
                            continue

                        fulltext.append(v)

                        if v2 not in map[field]:
                            map[field].append(v2)

                            

            for key in map:
                item[key] = map[key]

            item["thumbnail"] = member["thumbnail"]

            manifest = member["@id"]

            if "hi-nishikie" in manifest:
                manifest = manifest.replace("https://hi-nishikie.web.app", "https://hi-ut.github.io/dataset")
                manifest = manifest.replace("hi-nishikie-", "nishikie_hi-")
                manifest = manifest.replace("/api/", "/")

            item["manifest"] = manifest

            fields = ["images", "texts"]

            for f in fields:

                if f in member:
                    item[f] = []

                    for uri2 in member[f]:
                        item[f].append(hashlib.md5(uri2.encode('utf-8')).hexdigest())
                
            item["label"] = member["label"]
            fulltext.append(member["label"])

            item["attribution"] = member["attribution"]
            item["license"] = member["license"]

            item["fulltext"] = "|".join(fulltext)

            results.append(item)

            '''
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

    

with open("data/index.json", 'w') as outfile:
    json.dump(results, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))