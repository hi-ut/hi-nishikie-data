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

def download_img(url, file_name):
    result = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as web_file:
            data = web_file.read()
            with open(file_name, mode='wb') as local_file:
                local_file.write(data)
            print("--- downloaded", id)
    except urllib.error.URLError as e:
        print(id, url, e)
        result = [id, url, e]
    return result

files = glob.glob("../../../docs/api/iiif/collection/*.json")

for i in range(len(files)):

    file = files[i]

    with open(file) as f:
        collection = json.load(f)

    if "manifests" not in collection:
        continue

    manifests = collection["manifests"]
    
    for j in range(len(manifests)):
        m = manifests[j]

        id = m["@id"]
        thumbnail = ""

        id = hashlib.md5(id.encode('utf-8')).hexdigest()

        if "thumbnail" in m:
            if "@id" in m["thumbnail"]:
                thumbnail = m["thumbnail"]["@id"]
            else:
                thumbnail = m["thumbnail"]
        
        if thumbnail == "":
            continue

        path = "data/files/medium/"+id+".jpg"

        if not os.path.exists(path):
            print(j, len(manifests), i, len(files))
            download_img(thumbnail, path)
