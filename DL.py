import json
import base64
import os

cwd = os.getcwd()

def getQueryEntry(query: list, key: str):
    for entry in query:
        if entry["name"] == key:
            return entry["value"]

def buildFilename(query_info):
    deg = 0
    xcoord = int(getQueryEntry(query_info, "x"))
    ycoord = int(getQueryEntry(query_info, "y"))
    zcoord = int(getQueryEntry(query_info, "z"))
    filename = f"{deg}_{xcoord}_{ycoord}_{zcoord}"

    return filename


with open('.\\HARFILES\\flt.har', 'r', encoding="utf-8") as f:
    har_json = json.loads(f.read())

for i,entry in enumerate(har_json['log']["entries"]):
    if entry["response"]["content"]["mimeType"].find("image/jpeg") == 0:
        try:
            encoded_string = entry["response"]["content"]["text"]
            size = entry["response"]["content"]["size"]
            name = buildFilename(entry["request"]["queryString"])

            print(f"Found image {name} with size {size}")
        except KeyError:
            print("Key not found, skipping")
            continue

        filename = cwd + "\\" + "downloads" + "\\" + name + '.jpeg'

        with open(filename,'wb') as f:
            f.write(base64.b64decode(encoded_string))
