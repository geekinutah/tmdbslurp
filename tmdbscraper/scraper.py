import tmdbsimple as tmdb

#from pprint import pprint

class scraper:
    FREQUENCY = 10
    OPS_PER_TICK = 40

    def __init__(self, first_id=1, last_id=-1, api_key=None,
            frequency=FREQUENCY, operations=OPS_PER_TICK, *args, **kwargs):
        self.opcount = 0
        if self.api_key:
            tmdb.API_KEY = self.api_key
        else:
            raise(RuntimeError("You must specify an api_key"))

    def _get_episode_rating(self, episode, iso_3166_1='US'):
        to_return = "NR"
        for r in episode.content_ratings()['results']:
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
        for r in movie.releaseDates()['results']:
            if r['iso_3166_1'] == iso_3166_1:
                for d in r['release_dates']:
                    if d['type'] == 3:
                        to_return = d['release_date']
        return to_return

    def _get_movie_fields(self, movie):
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

    def _get_episode_fields(self, episode):
        to_return = {
                  'description' : episode.description,
                  'runtime' : episode.runtime,
                  'posters' : episode.posters(),
                  'backdrops': episode.backdrops(),
                  'rating' : self._get_episode_rating(episode),
                  'title' : episode.title(),
                  'tmdb_id' : episode.id,
                  'year' : episode.first_air_date,
                }
        return to_return

    def go(download_images=False, dump_to_sqlite=False, *args, **kwargs):
        pass

