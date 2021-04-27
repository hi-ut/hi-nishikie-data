import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import json
import hashlib

map = {}

with open("data/es.json") as f:
    data = json.load(f)

    for obj in data:
        source = obj["_source"]

        for key in source:
            values = source[key]

            for value in values:
                print(value)
                if not value:
                    continue

                if "http" in value:
                    es = [value]
                else:
                    es = value.split("/")

                if key not in map:
                    map[key] = {}

                for e in es:
                    if e not in map[key]:
                        map[key][e] = 0

                    map[key][e] += 1

map2 = {}
map3 = {}

for key in map:
    obj = map[key]

    obj_sorted = sorted(obj.items(), key=lambda x:x[1], reverse=True)

    obj2 = {}

    size = 0

    arr = []

    for i in range(len(obj_sorted)):

        e = obj_sorted[i]

        if i == 0 and e[1] == 1:
            break

        
        obj2[e[0]] = e[1]

        size += 1

        if i < 5:
            arr.append(e)

    map2["{}({})".format(key, size)] = obj2

    map3["{}({})".format(key, size)] = arr

with open("data/map.json", 'w') as outfile:
    json.dump(map2, outfile, ensure_ascii=False,
                indent=4, separators=(',', ': '))

with open("data/test.json", 'w') as outfile:
    json.dump(map3, outfile, ensure_ascii=False,
                indent=4, separators=(',', ': '))