#!/usr/bin/env python3

import argparse
from tmdbslurper import slurper
from tmdbslurper.slurper import slurper as slurpy
#from pprint import pprint

def start_slurping(first_id=1, last_id=-1, api_key=None,
        operations=slurper.OPS_PER_TICK, frequency=slurper.FREQUENCY,
        *args, **kwargs):
    s = slurpy(
            first_id=first_id,
            last_id=last_id,
            api_key=api_key,
            operations=operations,
            frequency=frequency)
    s.go(download_images=True)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--first-id",
            type=int,
            help="Starting movie ID to scrape",
            default=1)
    parser.add_argument("-l", "--last-id",
            type=int,
            help="Optional ending moving ID",
            default=-1)
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
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    start_slurping(args)
