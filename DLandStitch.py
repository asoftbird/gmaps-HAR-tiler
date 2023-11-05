import os
import re
import sys
import json
import base64
from PIL import Image

Image.MAX_IMAGE_PIXELS = 933120000
cwd = os.getcwd()
tile_dir = cwd + "\\" + "downloads"
tile_size = 256
harfile = "nimma_21.har"
#TODO: make input/output filename an argument

desired_zlevel = 21
output_image = "nimma_1" + "_" + str(desired_zlevel)

def buildInitialFilename(query_info):
    if desired_zlevel == 6:
        deg = 0
        xcoord = int(query_info[2]["value"])
        ycoord = int(query_info[3]["value"])
        zcoord = int(query_info[4]["value"])
        filename = f"{deg}_{xcoord}_{ycoord}_{zcoord}"

    else:
        deg = int(query_info[2]["value"])
        xcoord = int(query_info[3]["value"])
        ycoord = int(query_info[4]["value"])
        zcoord = int(query_info[5]["value"])
        filename = f"{deg}_{xcoord}_{ycoord}_{zcoord}"

    return filename, zcoord

def saveImages(infile, output_directory):
    with open(infile, 'r', encoding="utf-8") as f:
        har_json = json.loads(f.read())

    for i, entry in enumerate(har_json['log']["entries"]):
        if entry["response"]["content"]["mimeType"].find("image/jpeg") == 0:
            try:
                print(f"index: {i}")
                if entry["request"]["queryString"][0]["name"] == "v":
                    encoded_string = entry["response"]["content"]["text"]
                    size = entry["response"]["content"]["size"]
                    name, zcoord = buildInitialFilename(entry["request"]["queryString"])
                    print(f"Found image {name} with size {size} and zcoord {zcoord}")
                else:
                    continue

            except KeyError:
                print("Key not found, skipping")
                continue

            # except IndexError as e:
            #     print(f"{e}: skipping")
            #     continue

            if zcoord != desired_zlevel:
                print("Found image of wrong Z level, skipping")
                continue
            else:

                filename = output_directory + "\\" + name + '.jpeg'

                with open(filename,'wb') as f:
                    f.write(base64.b64decode(encoded_string))

def getCoordinates(filename):
    result = re.search(r"(\d*)_(\d*)_(\d*)_(\d*)", filename)
    return int(result.group(2)), int(result.group(3)), int(result.group(4))

def getMinMaxCoordinates(inputdir):
    x_list = []
    y_list = []

    for filename in os.listdir(inputdir):
        f = os.path.join(inputdir, filename)

        if os.path.isfile(f):
            xcoord, ycoord, zcoord = getCoordinates(filename)
            if zcoord == desired_zlevel:
                x_list.append(xcoord)
                y_list.append(ycoord)
            else:
                continue
    
    return min(x_list), max(x_list), min(y_list), max(y_list)


def stitchImages(inputdir):
    x_min, x_max, y_min, y_max = getMinMaxCoordinates(inputdir)
    width = (x_max - x_min + 1) * tile_size
    height = (y_max - y_min + 1) * tile_size

    if width > 100000 or height > 100000:
        sys.exit("Resulting image size too large. Dataset too big or coordinates don't match up. Aborting.")

    print(f"Resulting image size: {width}x{height}")

    result = Image.new('RGB', (width, height))

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tile_filename = inputdir + "\\" + f"0_{x}_{y}_{desired_zlevel}.jpeg"
            if os.path.exists(tile_filename):
                tile = Image.open(tile_filename)

                x_offset = (x - x_min) * tile_size
                y_offset = (y - y_min) * tile_size

                result.paste(tile, (x_offset, y_offset))

    result.save(f'{output_image}.jpg')

saveImages(harfile, tile_dir)
stitchImages(tile_dir)