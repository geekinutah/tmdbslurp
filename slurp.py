#!/usr/bin/env python3

import argparse
from tmdbslurper import slurper
from tmdbslurper.slurper import Slurper as slurpy
from pprint import pprint
import sys

def start_slurping(infile=None, outfile=None, api_key=None,
        operations=slurper.OPS_PER_TICK, frequency=slurper.FREQUENCY,
        *args, **kwargs):

    ids = infile.read().splitlines()
    s = slurpy(
            id_list=ids,
            api_key=api_key,
            operations=operations,
            frequency=frequency)
    pprint(s.go(download_images=True), stream=outfile)

def get_args():
    to_return = None
    list_format = 'Filename with list formatted like so:\nmovie-2\nseries-45netc.'
    parser = argparse.ArgumentParser()
    parser.add_argument('-infile', nargs='?', type=argparse.FileType('r'),
            default=sys.stdin,
            help=list_format)
    parser.add_argument('-outfile', nargs='?', type=argparse.FileType('w'),
            default=sys.stdout,
            help='JSON results, one object per line will be written out')
    parser.add_argument('-k', "--api-key",
            type=str,
            help="A valid TMDB API key")
    parser.add_argument('-o', "--operations",
            type=int,
            help="How many scrape operations per freq to perform",
            default=slurper.OPS_PER_TICK)
    parser.add_argument('-q', '--frequency',
            type=int,
            help="Frequency of operations in seconds",
            default=slurper.FREQUENCY)
    to_return = parser.parse_args()
    return to_return

if __name__ == "__main__":
    args = get_args()
    start_slurping(**vars(args))
