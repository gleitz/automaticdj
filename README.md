Automatic DJ
================================

Automatic music selection system for people
who love great music (even if they don't know it yet). Uses [facial recognition](http://developers.face.com/) and the [Hunch API](http://hunch.com/developers) to build a custom playlist based on the tastes of the people at the party.

The current version uses AppleScript to play the song using Spotify, but once the playlist is generated you can use any music player to play the track. There is also minimal support in the code for playing songs through the GrooveShark API.

Other libraries used include:

* [isightcapture](http://www.intergalactic.de/pages/iSight.html) for taking pictures via the command line
* [python-face-client](https://github.com/Kami/python-face-client) (edited to work with the current Face.com API)
* [EchoNest](http://code.google.com/p/pyechonest/)
* [Spotify Metadata API](http://developer.spotify.com/en/metadata-api/overview/)


Getting started
---------------

1. In `visage.py`
   * Edit the section titled "edit me!" with youe Face.com API key and secret, Facebook session key, Facebook ID, and Hunch auth token

2. Train your friends' faces
   * `import visage`
   * `visage.train("http://www.facebook.com/gleitz")

4. Take a photo, get the Facebook id of the user, get music recommendations from Hunch, and play the song using Spotify
   * `visage.musicify()`

Notes and gotchas
-----------------

* If you just want to test the photo -> FB id functionality, try calling `visage.recognize()`

* Getting a FB session is a bit of a pain. Here's what I did:
  1. Create a Facebook App
  2. Go to this link, inserting your client_id `https://graph.facebook.com/oauth/authorize?client_id=XXX&redirect_uri=http%3A//gleitzman.com/faces/&scope=offline_access,email,user_birthday,user_about_me,user_education_history,user_interests,user_likes,user_location,user_religion_politics,user_website,user_work_history,user_checkins,friends_about_me,friends_likes,friends_birthday,friends_education_history,friends_checkins,user_photo_video_tags,user_photos,friends_photo_video_tags,friends_photos,friends_birthday,friends_location,friends_work_history,friends_education_history,friends_activities,friends_hometown,friends_interests,friends_location,friends_likes`
  3. Exchange for an infinite session: `https://graph.facebook.com/oauth/access_token?client_id=XXX&redirect_uri=http%3A//gleitzman.com/faces/&client_secret=XXX`