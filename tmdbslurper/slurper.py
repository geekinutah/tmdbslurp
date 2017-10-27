import sys
import time
sys.path.append('..')

import tmdbsimple as tmdb
import logging

from requests.exceptions import HTTPError

FREQUENCY = 10
OPS_PER_TICK = 40


class Slurper(object):
    def __init__(self, id_list=None, api_key=None,
            frequency=FREQUENCY, operations=OPS_PER_TICK, *args, **kwargs):
        self.opcount = 0
        if api_key:
            tmdb.API_KEY = api_key
        else:
            raise(RuntimeError("You must specify an api_key"))
        self.id_list = id_list

    def _get_tv_rating(self, tv, iso_3166_1='US'):
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

        for r in movie.release_dates()['results']:
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
                  'description' : movie.info()['overview'],
                  'runtime' : movie.runtime,
                  'images': movie.images(),
                  'rating' : self._get_movie_rating(movie),
                  'title' : movie.title,
                  'tmdb_id' : movie.id,
                  'year' : self._get_movie_release_year(movie),
                }
        return to_return

    def _get_episode_fields(self, tv, episode):
        to_return = {
                  'description' : episode.info()['overview'],
                  'runtimes' : tv.info()['episode_runtime'],
                  'images' : episode.images(),
                  'rating' : self._get_tv_rating(tv),
                  'title' : episode.name,
                  'tmdb_id' : episode.id,
                  'year' : episode.air_date,
                }
        return to_return

    def _get_Movie(self, id=0, *args, **kwargs):
        if id:
          m = tmdb.Movies(id)
          return m

    def _get_Episode(self, series_id=0, season_num=0, episode_num=0,
            *args, **kwargs):
        if series_id and season_num and episode_num:
            e = tmdb.TV_Episodes(series_id, season_num, episode_num)
            return e

    def _get_TV(self, series_id=0, *args, **kwargs):
        if series_id:
            t = tmdb.TV(series_id)
            return t
    def _get_Series_children_matrix(self, series_id=0, *args, **kwargs):
        to_return = []
        while True:
            try:
                if series_id:
                    t = self._get_TV(series_id)
                    seasons = t.info()['seasons']
                    for s in seasons:
                        s_num = s['season_number']
                        e_count = s['episode_count']
                        for i in range(1, e_count):
                            to_return.append({
                                'season': s_num,
                                'episode': i})
            except HTTPError as h:
                status = int(h.response.status_code)
                if status  == 429:
                    sleep_for = int(
                            h.response.headers['Retry-After'])
                    time.sleep(sleep_for)
                    continue
            break

        return to_return

    def go(self, *args, **kwargs):
        to_return = { 'movies': [], 'episodes': [] }
        if not self.id_list:
            return to_return

        for i in self.id_list:
            (obj, obj_id) = i.split('-')
            if obj == 'series':
                for child in self._get_Series_children_matrix(obj_id):
                    while True:
                        try:
                            e = self._get_Episode(obj_id,
                                    child['season'], child['episode'])
                            t = self._get_TV(obj_id)
                            if e is None:
                                logging.debug("TV Series ID: %s" % i)
                                logging.debug(
                                        "Episode %s, season %s is None" % (
                                            child['season'],
                                            child['episode']))
                            results = self._get_episode_fields(t, e)
                            to_return['episodes'].append(results)
                        except HTTPError as h:
                            status = int(h.response.status_code)
                            if status  == 429:
                                sleep_for = int(
                                        h.response.headers['Retry-After'])
                                time.sleep(sleep_for)
                                continue
                        break
            elif obj == 'movie':
                    while True:
                        try:
                            results = self._get_movie_fields(
                                self._get_Movie(obj_id))
                            to_return['movies'].append(results)
                        except HTTPError as h:
                            status = int(h.response.status_code)
                            if status  == 429:
                                sleep_for = int(
                                        h.response.headers['Retry-After'])
                                time.sleep(sleep_for)
                                continue
                        break

        return to_return

