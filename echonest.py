import os
import simplejson
import urllib
import urllib2
import logging
from pyechonest import config, artist, song

logging.basicConfig(level=logging.DEBUG)
config.ECHO_NEST_API_KEY="OCQQQWJBKZXHKPXHZ"

def prompt():
    userinput = raw_input("Gimme an artist: ")
    if not userinput:
        exit()
    
    print dance_songs(get_artist_id(userinput))

def get_artist_id(artist_name):
    result = artist.search(name=artist_name)
    if not result:
        return False
    return result[0].id

def dance_songs(artist_id, dance=0.6, maxresults=10):
    results = song.search(artist_id=artist_id,
                          min_danceability=dance,
                          results=maxresults,
                          sort='danceability-desc',
                          buckets=['audio_summary'])
    return results



if __name__ == '__main__':
    prompt()
    
                                         
