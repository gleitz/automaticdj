import hmac
import os
import random
import simplejson
import sys
import urllib
import urllib2
import traceback
from face_client import face_client
from pyechonest import config, artist, song

SPOTIFY_BASE_URL = 'http://ws.spotify.com/search/1/%s.json?q=%s'

# edit me!
FACE_API_KEY = ''
FACE_API_SECRET = ''
FB_SESSION_KEY = ''
FB_USER = ''
ISIGHTCAPTURE_PATH = '/usr/local/bin/isightcapture'
HUNCH_AUTH_TOKEN = ''

# for grooveshark
GROOVESHARK_SESSION_ID = ''
GROOVESHARK_API_KEY = ''
GROOVESHARK_SECRET = ''
GROOVESHARK_BASE_URL = 'http://api.grooveshark.com/ws/2.1/'
config.ECHO_NEST_API_KEY= ''

SPOTIFY_SCRIPT_SONG = """osascript<<END
on spotify_exec(command)
	if command is "mute" then set menu_item to 10
	if command is "unmute" then set menu_item to 9
	tell application "Spotify" to activate
	tell application "System Events"
		tell process "Spotify"
			repeat 10 times
				click menu item menu_item of menu 1 of menu bar item 6 of menu bar 1
			end repeat
		end tell
	end tell
end spotify_exec

spotify_exec("mute")
open location "%s"
say "%s is in the house!"

tell application "Spotify" to activate
tell application "System Events"
	tell process "Spotify"
		my spotify_exec("unmute")
                -- tell application "System Events" to set visible of process "Spotify" to false
	end tell
end tell
"""

SPOTIFY_SCRIPT = """osascript<<END
on spotify_exec(command)
	if command is "mute" then set menu_item to 10
	if command is "unmute" then set menu_item to 9
	tell application "Spotify" to activate
	tell application "System Events"
		tell process "Spotify"
			repeat 10 times
				click menu item menu_item of menu 1 of menu bar item 6 of menu bar 1
			end repeat
		end tell
	end tell
end spotify_exec

spotify_exec("mute")
open location "%s"
say "%s is in the house!"

tell application "Spotify" to activate
tell application "System Events"
	tell process "Spotify"
		keystroke "l" using {command down}
		repeat 3 times
			keystroke tab
		end repeat
		repeat %d times
			key code {125}
		end repeat
		keystroke return
		my spotify_exec("unmute")
                -- tell application "System Events" to set visible of process "Spotify" to false
	end tell
end tell
"""

def recognize(live=True, path='/tmp/pic.jpg'):
    client = face_client.FaceClient(FACE_API_KEY, FACE_API_SECRET)
    client.set_facebook_credentials(session=FB_SESSION_KEY, user=FB_USER)
    if live:
        os.system('%s %s' % (ISIGHTCAPTURE_PATH, path))
    result = client.faces_recognize(file=path, uids='friends@facebook.com', aggressive=True)
    if not result:
        return 'Could not recognize face'
    try:
        print [uid for uid in result['photos'][0]['tags'][0]['uids'][:5]]
        uid = result['photos'][0]['tags'][0]['uids'][0]['uid']
    except:
        return result

    uid = uid.replace('@facebook.com', '')
    fb_result = fetch_url('http://graph.facebook.com/' + uid)
    if not fb_result:
        return 'Could not contact facebook'
    fb_result = simplejson.loads(fb_result)
    print '\n\n\nHello, %s\n\n\n' % (fb_result['name'])
    return {'uid': uid, 'name': fb_result['name']}

def train(url):
    print 'training...'
    client = face_client.FaceClient(FACE_API_KEY, FACE_API_SECRET)
    client.set_facebook_credentials(session=FB_SESSION_KEY, user=FB_USER)
    if 'profile.php' in url:
        id = url[url.find('id=') + 3:]
        result = client.faces_train(uids='%s@facebook.com' % (id))
        return result
    url = url.replace('www.facebook.com', 'graph.facebook.com')
    result = fetch_url(url)
    if not result:
        return 'Could not train'
    id = simplejson.loads(result).get('id')
    result = client.faces_train(uids='%s@facebook.com' % (id))
    return result

def debug_print(string):
    print '!'*80
    print string
    print '!'*80


def musicify(live=True, uid=None):
    result = {}
    name = ''
    if not uid:
        result = recognize(live=live)
        uid = result.get('uid')
        name = result.get('name')
        if not uid or type(uid) == dict:
            return 'Sorry, could not recognize face'

    fb_id = 'fb_' + uid

    # recs = get_recs('hn_t32564', fb_id)
    if not uid == '5552189986':
        recs = get_recs('list_musician', fb_id)
    else:
        recs = {'recommendations':[{'name':'Loscil'},{'name':'School of Seven Bells'},{'name':'Gold Panda'},{'name':'Solvent'},{'name':'Tycho'},{'name':'Lusine'}]}
    worked = False
    song_name = ''
    artist = ''
    while not worked:
        try:
            artist = random.choice(recs.get('recommendations')).get('name')
            debug_print(artist)
            # Uncomment to use the Echonest API
            # artist_id = echonest_artist_id(artist)
            # debug_print(artist_id)
            # songs = echonest_dance_songs(artist_id)
            if False:
                success = False
                num_tries = 0
                while not success and num_tries < 9:
                    song_choice = random.choice(songs)
                    song_name = song_choice.title
                    song = ' '.join([artist, song_name])
                    try:
                        spotify_queue_type('track', song, name=name)
                        success = True
                    except:
                        num_tries += 1
                        continue

            else:
                spotify_queue_type('artist', artist, name=name)

            worked = True
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            pass

    result['artist'] = artist
    result['title'] = song_name
    return result


def get_recs(topic_id, user_id):
    url = 'http://api.hunch.com/api/v1/get-recommendations/?topic_ids=%s&limit=10&group_user_ids=%s&minimal=1&popularity=0&auth_token=%s' % (topic_id, user_id, HUNCH_AUTH_TOKEN)
    return simplejson.loads(fetch_url(url))

def spotify_queue(href, name=''):
    os.system(SPOTIFY_SCRIPT % (href, name or 'Automatic DJ', random.randint(0,10)))

def spotify_queue_song(href, name=''):
    debug_print(href)
    debug_print("song!!!!")
    os.system(SPOTIFY_SCRIPT_SONG % (href, name or 'Automatic DJ'))

def spotify_queue_type(music_type, query, name=''):
    url = SPOTIFY_BASE_URL % (music_type, urllib.quote(query))
    result = fetch_url(url)
    if not result:
        return False
    result = simplejson.loads(result)
    href = result.get(music_type + 's')[0].get('href')
    spotify_queue(href, name)

def spotify_queue_album(query, name=''):
    url = SPOTIFY_BASE_URL % ('album', urllib.quote(query))
    result = fetch_url(url)
    if not result:
        return False
    result = simplejson.loads(result)
    href = result.get('albums')[0].get('artists')[0].get('href')
    spotify_queue(href, name)

def spotify_queue_artist(query, name=''):
    url = SPOTIFY_BASE_URL % ('artist', urllib.quote(query))
    result = fetch_url(url)
    if not result:
        return False
    result = simplejson.loads(result)
    href = result.get('albums')[0].get('artists')[0].get('href')
    spotify_queue(href, name)

def spotify_prompt():
    artist = raw_input('What artist would you like to hear today? ')
    spotify_queue_type('artist', artist)

def echonest_artist_id(artist_name):
    result = artist.search(name=artist_name)
    if not result:
        return False
    return result[0].id

def echonest_dance_songs(artist_id, dance=0.6, maxresults=10):
    return song.search(artist_id=artist_id,
                       min_danceability=dance,
                       results=maxresults,
                       sort='danceability-desc',
                       buckets=['audio_summary'])

def fetch_url(url, values=None):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.94 Safari/534.13'
    headers = {'User-Agent': user_agent}
    if values:
        data = urllib.urlencode(values).replace('%5B', '[').replace('%5D', ']')
    else:
        data = ''
    print url

    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

def gs_sign_request(method, dict_object):
    test = ''
    code = hmac.new(GROOVESHARK_SECRET)
    code.update(method)
    test += method
    # encoded_args = sorted([(k.encode('utf-8') if type(k) in [str,unicode] else str(k), v.encode('utf-8') if type(v) in [str,unicode] else (flatten_dict(v) if type(v) in [dict] else str(v))) for k, v in dict_object.items()])
    encoded_args = []
    for key, value in encoded_args:
        code.update(key)
        code.update(value)
        test += key
        test += value
    print "!"*80
    print test
    print "!"*80
    return code.hexdigest()

def flatten_dict(dict_object):
    string = ''
    for k, v in dict_object.items():
        string += k.encode('utf-8') + v.encode('utf-8')
    return string

def gs_call_method(method, dict_object, format='json'):
    dict_object['sessionID'] = GROOVESHARK_SESSION_ID
    data = {}
    data.update(dict_object)
    data['method'] = method
    data['sig'] = gs_sign_request(method, dict_object)
    data['format'] = format
    data['wsKey'] = GROOVESHARK_API_KEY
    return data

def gs_country():
    return {'country[ID]': '223',
            'country[CC1]': '0',
            'country[CC3]': '0',
            'country[CC2]': '0',
            'country[CC4]': '1073741824',
            'country[IPR]': '3949'}

def gs_get_song():
    songid = 145992
    method = 'getSubscriberStreamKey'

    params = {}
    params['songID'] = songid
    params['lowBitrate'] = 0
    params = gs_call_method(method, params)

    sigparams = {"country": "ID223CC10CC20CC30CC41073741824IPR3949",
                 "songID": songid,
                 "lowBitrate": '0',
                 "sessionID": GROOVESHARK_SESSION_ID}

    print params
    params['sig'] = gs_sign_request(method, sigparams)

    querystring = urllib.urlencode(params) + '&country[ID]=223&country[CC1]=0&country[CC2]=0&country[CC3]=0&country[CC4]=1073741824&country[IPR]=3949'
    url = GROOVESHARK_BASE_URL + '?' + querystring

    print url
    res = fetch_url(url)

    print res


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'recognize':
        recognize()
    else:
        os.system('clear')
        spotify_prompt()
