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

dir = "../../../docs/api/iiif/curation"

path = dir + "/test.json"

path2 = dir + "/top_text_tmp.json"

text_map = {}

with open(path2) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            text_map[member["@id"]] = member["texts"]

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            id = member["@id"]

            if id in text_map:
                member["texts"] = text_map[id]

path = dir + "/top_text.json"

with open(path, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))