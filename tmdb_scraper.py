#!/bin/env python3

import argparse
import tmdbsimple as tmdb

#NOTE(mwilson): Not needed so far, we can get all from API
#from bs4 import BeautifulSoup
from pprint import pprint
from threading import Timer



class TMDBScraper:
    FREQUENCY = 10
    OPS_PER_TICK = 40

    def __init__(self, **kwargs):
        self.opcount = 0
        self.timer = kwargs['timer'] or Timer()
        self.first = kwargs['first'] or 1
        self.last = kwargs['last'] or -1
        self.api_key = kwargs['api_key'] or None
        self.freq = kwargs['frequency'] or TMDBScraper.FREQUENCY
        self.operations = kwargs['operations'] or TMDBScraper.OPS_PER_TICK
        if self.api_key:
            tmdb.API_KEY = self.api_key

    def _get_movie_rating(self, movie, iso_3166_1='US'):
        to_return = "NR"
        for r in movie.releases()['countries']:
            if r['iso_3166_1'] == iso_3166_1:
                to_return = r['certification']

        return to_return

    def _get_movie_release_year(self, movie, iso_3166_1='US'):
        to_return = None
        path = m._get_id_path('release_dates')
        response = m._GET(path)
        m._set_attrs_to_values(response)
        for r in response['results']:
            if r['iso_3166_1'] == iso_3166_1:
                for d in r['release_dates']:
                    if d['type'] == 3:
                        to_return = d['release_date']
                        #XXX(mwilson): This is assuming that we only care about movies that had a Theatrical release?

       return to_return

    def movie_fields(self, movie):
        to_return = {
                  'description' : movie.description,
                  'runtime' : movie.runtime,
                  'posters' : movie.posters(),
                  'backdrops': movie.backdrops(),
                  'rating' : self._get_movie_rating(movie),
                  'title' : movie.title(),
                  'tmdb_id' : movie.id,
                  'year' : self._get_movie_release_year(movie),
                }
        return to_return

    def episode_fields(self, episode):
        pass

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
            default=TMDBScraper.OPS_PER_TICK)
    parser.add_argument('-q', '--frequency',
            type=int,
            help="Frequency of operations in seconds",
            default=TMDBScraper.FREQUENCY)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    pprint(args)
