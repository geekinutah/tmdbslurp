import sqlite3

import tmdbsimple as tmdb

#from pprint import pprint

FREQUENCY = 10
OPS_PER_TICK = 40

class slurper:

    def __init__(self, first_id=1, last_id=-1, id_list=None, api_key=None,
            frequency=FREQUENCY, operations=OPS_PER_TICK, *args, **kwargs):
        self.opcount = 0
        if api_key:
            tmdb.API_KEY = self.api_key
        else:
            raise(RuntimeError("You must specify an api_key"))

    def _get_episode_rating(self, tv, iso_3166_1='US'):
        to_return = "NR"
        for r in tv.content_ratings()['results']:
            if r['iso_3166_1'] == iso_3166_1:
                to_return = r['rating']
        return to_return

    def _get_movie_rating(self, movie, iso_3166_1='US'):
        to_return = "NR"
        for r in movie.releases()['countries']:
            if r['iso_3166_1'] == iso_3166_1:
                to_return = r['certification']

        return to_return

    def _get_movie_release_year(self, movie, iso_3166_1='US'):
        to_return = None
        limited_theatrical = None
        theatrical = None
        digital = None
        physical = None

        for r in movie.releaseDates()['results']:
            if r['iso_3166_1'] == iso_3166_1:
                for d in r['release_dates']:
                    if d['type'] == 2:
                        limited_theatrical = d['release_date']
                    elif d['type'] == 3:
                        theatrical = d['release_date']
                    elif d['type'] == 4:
                        digital = d['release_date']
                    elif d['type'] == 5:
                        physical = d['release_date']

        if theatrical:
            to_return = theatrical
        elif limited_theatrical:
            to_return = limited_theatrical
        elif physical:
            to_return = physical
        elif digital:
            to_return = digital

        return to_return

    def _get_movie_fields(self, movie):
        to_return = {
                  'description' : movie.description,
                  'runtime' : movie.runtime,
                  'images': movie.images(),
                  'rating' : self._get_movie_rating(movie),
                  'title' : movie.title(),
                  'tmdb_id' : movie.id,
                  'year' : self._get_movie_release_year(movie),
                }
        return to_return

    def _get_episode_fields(self, tv, episode):
        to_return = {
                  'description' : episode.overview,
                  'runtime' : episode.runtime,
                  'images' : episode.images(),
                  'rating' : self._get_tv_rating(tv),
                  'title' : episode.name,
                  'tmdb_id' : episode.id,
                  'year' : episode.air_date,
                }
        return to_return

    def go(download_images=False, dump_to_sqlite=None, *args, **kwargs):
        """
        Thoughts:
            if there is an ids array, go slurp things only in that array.
            if there is a first and a negative last, just go slurp in order.
            if there is a first and a last, only slurp in that range.
        """
        if dump_to_sqlite:
            sqlite3.connect(dump_to_sqlite)
            """Do stuff here"""
        pass

