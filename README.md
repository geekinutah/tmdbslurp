# tmdbslurp

Uses the TMDB API to get information about movies and episodes

## Instructions

$ ./slurp.py --help
usage: slurp.py [-h] [-infile [INFILE]] [-outfile [OUTFILE]] [-k API_KEY]
                [-o OPERATIONS] [-q FREQUENCY]

optional arguments:
  -h, --help            show this help message and exit
  -infile [INFILE]      Filename with list formatted like so: movie-2
                        series-45netc.
  -outfile [OUTFILE]    JSON results, one object per line will be written out
  -k API_KEY, --api-key API_KEY
                        A valid TMDB API key
  -o OPERATIONS, --operations OPERATIONS
                        How many scrape operations per freq to perform
  -q FREQUENCY, --frequency FREQUENCY
                        Frequency of operations in seconds



slurp wants a list of ids that looks like this:

movie-23489
movie-32478
series-1937
series-3837

* First column indicates what kind of id we have
* Second column indicates the id of the work

Slurp will retrieve information about movies and spit them out on stdout or -outfile.
In the case of series, Slurp will retrieve similar information, but for every episode in the series.


## Authors

* **Mike Wilsonn** - *Initial work* - [geekinutah](https://github.com/geekinutah)

## Acknowledgments

* Thanks to [celiao](https://github.com/celiao/tmdbsimple) for original implementation of tmdbsimple

