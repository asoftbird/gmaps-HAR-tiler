import json
import base64
import os

cwd = os.getcwd()

def buildFilename(query_info):
    deg = query_info[2]["value"]
    xcoord = query_info[3]["value"]
    ycoord = query_info[4]["value"]
    zcoord = query_info[5]["value"]
    filename = f"{deg}_{xcoord}_{ycoord}_{zcoord}"

    return filename


with open('source.har', 'r', encoding="utf-8") as f:
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
