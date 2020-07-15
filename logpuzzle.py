#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse
from operator import itemgetter


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    puzzle_urls = []
    with open(filename) as f: 
       text = f.read()
    pattern = r'/edu\S+.jpg'
    puzzle_paths = re.findall(pattern, text)
    for path in puzzle_paths:
        paths = 'http://code.google.com' + path
        puzzle_urls.append(paths)
    return sorted(list(dict.fromkeys(puzzle_urls)), key=lambda url: url[78:])
    
    #server_name = 'http://' + re.search(r'code.google.com', filename)
    #key=r'\w\w\w\w.jpg'

def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    img_name = []
    os.makedirs(dest_dir)
    os.chdir(dest_dir)
    for i in range(len(img_urls)):
        print("Retrieve... " + "img" + str(i) + ".jpeg")
        urllib.request.urlretrieve(img_urls[i], "img" + str(i) + ".jpeg")
        img_name.append("img" + str(i) + ".jpeg")
    with open('index.html', 'w') as f:
        f.write('<html><body>')
        for link in img_name:
            f.write(f"<img src='{link}'></img>")
        f.write('</body></html>')

    


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

# ANSWERS: Easter Bunny, Eiffel Tower