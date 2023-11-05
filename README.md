Usage: Open a google maps embedded view and traverse the map to get the tiles you want to download.
Open Dev Tools and use "Save All As HAR" to save all metadata of the tiles to a .har file. 

Run DLandStitch.py with a HAR file selected (must be edited in file, for now) to download all tiles & also stitch them together into one image.

To get a high resolution map, zoom in as far as you can before moving around, so you only get the maximum zoom level tiles. 