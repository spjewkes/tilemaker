#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool for breaking up images into a tileset.
"""
__version__ = 1.0

import argparse
import logging
import hashlib
import io
from PIL import Image

def create_hash(image):
    hash = hashlib.md5()
    with io.BytesIO() as byte_io:
        image.save(byte_io, 'TGA')
        data = byte_io.getvalue()
        hash.update(data)

    return hash.hexdigest()

def best_root(count):
    nearest_root = 0
    while (nearest_root + 1) ** 2 < count:
        nearest_root += 1
    return nearest_root + 1

def _main():
    """
    Application entrypoint when executing the script directly.
    """
    parser = argparse.ArgumentParser(description='Utility for processing images into a tileset.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+', help='File to process into a tileset')
    parser.add_argument('--width', metavar='WIDTH', type=int, default=8, help='Pixel width of the tiles to create')
    parser.add_argument('--height', metavar='HEIGHT', type=int, default=8, help='Pixel height of the tiles to create')
    parser.add_argument('--verbose', action='store_true', help='Produces verbose logging')
    parser.add_argument('--output', metavar='OUTFILE', type=str, default='output.png', help='Output file to write tiles to')
    
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

    tiles = dict()
        
    for image_file in args.files:
        with Image.open(image_file) as image:
            logging.info("Processing file: '{}' size: {}".format(image_file, image.size))

            for y in range(0, image.size[1], args.height):
                for x in range(0, image.size[0], args.width):
                    new_image = image.crop((x, y, x + args.width, y + args.height))
                    
                    hash = create_hash(new_image)
                    if hash not in tiles.keys():
                        tiles[hash] = new_image

    best_size = best_root(len(tiles))
    width = best_size * args.width
    height = best_size * args.height
    output_image = Image.new("RGB", (width, height))

    x, y = 0, 0
    
    for tile in tiles.values():
        output_image.paste(tile, (x, y))
        x += args.width
        if x >= width:
            x = 0
            y += args.height
    
    output_image.save(args.output)

if __name__ == "__main__":
    _main()
