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

files = glob.glob("manifests/*.json")
files = sorted(files)
from PIL import Image
import shutil

prefix0 = "https://hi-nishikie.web.app"
static_dir = "../../../static"

for file in files:
    print("-------------")
    print(file)
    
    json_open = open(file, 'r')
    df = json.load(json_open)

    id = df["@id"].split("/")[-1].split(".")[0]

    df["@id"] = prefix0 + "/api/iiif/rekihaku/" + id + "/manifest.json"

    df["thumbnail"]["@id"] =  df["thumbnail"]["@id"].replace("ext/nishikie/", "ext%2Fnishikie%2F")
    
    f_path = df["@id"].replace(prefix0, static_dir)
    dirname = os.path.dirname(f_path)
    os.makedirs(dirname, exist_ok=True)

    with open(f_path, 'w') as outfile:
        json.dump(df, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))