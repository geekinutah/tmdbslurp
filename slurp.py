#!/usr/bin/env python3

import argparse
from tmdbslurper import slurper
from tmdbslurper.slurper import Slurper as slurpy
from pprint import pprint
import sys

def start_slurping(first_id=1, last_id=-1, api_key=None,
        operations=slurper.OPS_PER_TICK, frequency=slurper.FREQUENCY,
        *args, **kwargs):
    s = slurpy(
            first_id=first_id,
            last_id=last_id,
            api_key=api_key,
            operations=operations,
            frequency=frequency)
    pprint(s.go(download_images=True))

def get_args():
    to_return = None
    list_format = 'Filename with list formatted like so:\nmovie-2\nseries-45netc.'
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs='?', type=argparse.FileType('r'),
            default=sys.stdin,
            help=list_format)
    parser.add_argument('-o', nargs='?', type=argparse.FileType('w'),
            default=sys.stdout,
            help='JSON results, one object per line will be written out')
    parser.add_argument('-k', "--api-key",
            type=int,
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
    start_slurping(args)
