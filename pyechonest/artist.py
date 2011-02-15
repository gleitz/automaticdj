#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2010-04-25.

The Artist module loosely covers http://developer.echonest.com/docs/v4/artist.html
Refer to the official api documentation if you are unsure about something.
"""
import util
from proxies import ArtistProxy, ResultList
from song import Song


class Artist(ArtistProxy):
    """
    An Artist object
    
    Attributes: 
        id (str): Echo Nest Artist ID
        
        name (str): Artist Name
        
        audio (list): Artist audio
        
        biographies (list): Artist biographies
        
        blogs (list): Artist blogs
        
        familiarity (float): Artist familiarity
        
        hotttnesss (float): Artist hotttnesss
        
        images (list): Artist images
        
        news (list): Artist news
        
        reviews (list): Artist reviews
        
        similar (list): Similar Artists
        
        songs (list): A list of song objects
        
        terms (list): Terms for an artist
        
        urls (list): Artist urls
        
        video (list): Artist video
        
    You create an artist object like this:
    
    >>> a = artist.Artist('ARH6W4X1187B99274F')
    >>> a = artist.Artist('the national')
    >>> a = artist.Artist('musicbrainz:artist:a74b1b7f-71a5-4011-9441-d0b5e4122711')
        
    """

    def __init__(self, id, **kwargs):
        """
        Artist class
        
        Args:
            id (str): an artistw ID 
            
        Returns:
            An artist object
            
        Example:
        
        >>> a = artist.Artist('ARH6W4X1187B99274F', buckets=['hotttnesss'])
        >>> a.hotttnesss
        0.80098515900997658
        >>>
        
        """
        super(Artist, self).__init__(id, **kwargs)    
    
    def __repr__(self):
        return "<%s - %s>" % (self._object_type.encode('utf-8'), self.name.encode('utf-8'))
    
    def __str__(self):
        return self.name.encode('utf-8')
    
    def __cmp__(self, other):
        return cmp(self.id, other.id)
    
    def get_audio(self, results=15, start=0, cache=True):
        """Get a list of audio documents found on the web related to an artist
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
        
        Returns:
            A list of audio document dicts; list contains additional attributes 'start' and 'total'
        
        Example:

        >>> a = artist.Artist('alphabeat')
        >>> a.get_audio()[0]
        {u'artist': u'Alphabeat',
         u'date': u'2010-04-28T01:40:45',
         u'id': u'70be4373fa57ac2eee8c7f30b0580899',
         u'length': 210.0,
         u'link': u'http://iamthecrime.com',
         u'release': u'The Beat Is...',
         u'title': u'DJ',
         u'url': u'http://iamthecrime.com/wp-content/uploads/2010/04/03_DJ_iatc.mp3'}
        >>> 
        """
        
        if cache and ('audio' in self.cache) and results==15 and start==0:
            return self.cache['audio']
        else:
            response = self.get_attribute('audio', results=results, start=start)
            if results==15 and start==0:
                self.cache['audio'] = ResultList(response['audio'], 0, response['total'])
            return ResultList(response['audio'], start, response['total'])
    
    audio = property(get_audio)
    
    def get_biographies(self, results=15, start=0, license='unknown', cache=True):
        """Get a list of artist biographies
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
            
            license (str): A string specifying the desired license type
        
        Returns:
            A list of biography document dicts; list contains additional attributes 'start' and 'total'
            
        Example:

        >>> a = artist.Artist('britney spears')
        >>> bio = a.get_biographies(results=1)[0]
        >>> bio['url']
        u'http://www.mtvmusic.com/spears_britney'
        >>> 
        """
        if cache and ('biographies' in self.cache) and results==15 and start==0 and license=='unknown':
            return self.cache['biographies']
        else:
            response = self.get_attribute('biographies', results=results, start=start, license=license)
            if results==15 and start==0 and license=='unknown':
                self.cache['biographies'] = ResultList(response['biographies'], 0, response['total'])
            return ResultList(response['biographies'], start, response['total'])
    
    biographies = property(get_biographies)    
    
    def get_blogs(self, results=15, start=0, cache=True, high_relevance=False):
        """Get a list of blog articles related to an artist
        
        Args:
            
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An ingteger starting value for the result set
        
        Returns:
            A list of blog document dicts; list contains additional attributes 'start' and 'total'
        
        Example:
        
        >>> a = artist.Artist('bob marley')
        >>> blogs = a.get_blogs(results=1,start=4)
        >>> blogs.total
        4068
        >>> blogs[0]['summary']
        But the Kenyans I know relate to music about the same way Americans do. They like their Congolese afropop, 
        and I've known some to be big fans of international acts like <span>Bob</span> <span>Marley</span> and Dolly Parton. 
        They rarely talk about music that's indigenous in the way a South African or Malian or Zimbabwean would, and it's 
        even rarer to actually hear such indigenous music. I do sometimes hear ceremonial chanting from the Maasai, but only 
        when they're dancing for tourists. If East Africa isn't the most musical part ... "
        >>> 
        """

        if cache and ('blogs' in self.cache) and results==15 and start==0 and not high_relevance:
            return self.cache['blogs']
        else:
            if high_relevance:
                high_relevance = 'true'
            else:
                high_relevance ='false'
            response = self.get_attribute('blogs', results=results, start=start, high_relevance=high_relevance)
            if results==15 and start==0:
                self.cache['blogs'] = ResultList(response['blogs'], 0, response['total'])
            return ResultList(response['blogs'], start, response['total'])
    
    blogs = property(get_blogs)
       
    def get_familiarity(self, cache=True):
        """Get our numerical estimation of how familiar an artist currently is to the world
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            A float representing familiarity.
        
        Example:

        >>> a = artist.Artist('frank sinatra')
        >>> a.get_familiarity()
        0.65142555825947457
        >>> a.familiarity
        0.65142555825947457
        >>>
        """
        if not (cache and ('familiarity' in self.cache)):
            response = self.get_attribute('familiarity')
            self.cache['familiarity'] = response['artist']['familiarity']
        return self.cache['familiarity']
    
    familiarity = property(get_familiarity)    

    def get_foreign_id(self, idspace='musicbrainz', cache=True):
        """Get the foreign id for this artist for a specific id space
        
        Args:
        
        Kwargs:
            idspace (str): A string indicating the idspace to fetch a foreign id for.
        
        Returns:
            A foreign ID string
        
        Example:
        
        >>> a = artist.Artist('fabulous')
        >>> a.get_foreign_id('7digital')
        u'7digital:artist:186042'
        >>> 
        """
        if not (cache and ('foreign_ids' in self.cache) and filter(lambda d: d.get('catalog') == idspace, self.cache['foreign_ids'])):
            response = self.get_attribute('profile', bucket=['id:'+idspace])
            foreign_ids = response['artist'].get("foreign_ids", [])
            self.cache['foreign_ids'] = self.cache.get('foreign_ids', []) + foreign_ids
        cval = filter(lambda d: d.get('catalog') == idspace, self.cache.get('foreign_ids'))
        if cval:
            return cval[0].get('foreign_id')
        else:
            return None
    
    def get_hotttnesss(self, cache=True):
        """Get our numerical description of how hottt an artist currently is
        
        Args:
            
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
        
        Returns:
            float: the hotttnesss value
        
        Example:
        
        >>> a = artist.Artist('hannah montana')
        >>> a.get_hotttnesss()
        0.59906022155998995
        >>> a.hotttnesss
        0.59906022155998995
        >>>
        """
        if not (cache and ('hotttnesss' in self.cache)):
            response = self.get_attribute('hotttnesss')
            self.cache['hotttnesss'] = response['artist']['hotttnesss']
        return self.cache['hotttnesss']
    
    hotttnesss = property(get_hotttnesss)
    
    def get_images(self, results=15, start=0, license='unknown', cache=True):
        """Get a list of artist images
        
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
            
            license (str): A string specifying the desired license type
        
        Returns:
            A list of image document dicts; list contains additional attributes 'start' and 'total'
        
        Example:
        
        >>> a = artist.Artist('Captain Beefheart')
        >>> images = a.get_images(results=1)
        >>> images.total
        49
        >>> images[0]['url']
        u'http://c4.ac-images.myspacecdn.com/images01/5/l_e1a329cdfdb16a848288edc6d578730f.jpg'
        >>> 
        """
        
        if cache and ('images' in self.cache) and results==15 and start==0 and license=='unknown':
            return self.cache['images']
        else:
            response = self.get_attribute('images', results=results, start=start, license=license)
            if results==15 and start==0 and license=='unknown':
                self.cache['images'] = ResultList(response['images'], 0, response['total'])
            return ResultList(response['images'], start, response['total'])
    
    images = property(get_images)    
    
    def get_news(self, results=15, start=0, cache=True, high_relevance=False):
        """Get a list of news articles found on the web related to an artist
        
        Args:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
        
        Returns:
            A list of news document dicts; list contains additional attributes 'start' and 'total'
        
        Example:
        
        >>> a = artist.Artist('Henry Threadgill')
        >>> news = a.news
        >>> news.total
        41
        >>> news[0]['name']
        u'Jazz Journalists Association Announces 2010 Jazz Award Winners'
        >>> 
        """
        if cache and ('news' in self.cache) and results==15 and start==0 and not high_relevance:
            return self.cache['news']
        else:
            if high_relevance:
                high_relevance = 'true'
            else:
                high_relevance = 'false'                
            response = self.get_attribute('news', results=results, start=start, high_relevance=high_relevance)
            if results==15 and start==0:
                self.cache['news'] = ResultList(response['news'], 0, response['total'])
            return ResultList(response['news'], start, response['total'])
    
    news = property(get_news)
    
    def get_reviews(self, results=15, start=0, cache=True):
        """Get reviews related to an artist's work
        
        Args:
            
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
        
        Returns:
            A list of review document dicts; list contains additional attributes 'start' and 'total'
        
        Example:
        
        >>> a = artist.Artist('Ennio Morricone')
        >>> reviews = a.reviews
        >>> reviews.total
        17
        >>> reviews[0]['release']
        u'For A Few Dollars More'
        >>> 
        """
        if cache and ('reviews' in self.cache) and results==15 and start==0:
            return self.cache['reviews']
        else:
            response = self.get_attribute('reviews', results=results, start=start)
            if results==15 and start==0:
                self.cache['reviews'] = ResultList(response['reviews'], 0, response['total'])
            return ResultList(response['reviews'], start, response['total'])
    
    reviews = property(get_reviews)
    
    def get_similar(self, results=15, start=0, buckets=None, limit=False, cache=True, max_familiarity=None, min_familiarity=None, \
                    max_hotttnesss=None, min_hotttnesss=None, min_results=None, reverse=False):
        """Return similar artists to this one
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
            
            max_familiarity (float): A float specifying the max familiarity of artists to search for
            
            min_familiarity (float): A float specifying the min familiarity of artists to search for
            
            max_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
            
            min_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
            
            reverse (bool): A boolean indicating whether or not to return dissimilar artists (wrecommender). Defaults to False.
        
        Returns:
            A list of similar Artist objects
        
        Example:
        
        >>> a = artist.Artist('Sleater Kinney')
        >>> similars = a.similar[:5]
        >>> similars
        [<artist - Bikini Kill>, <artist - Pretty Girls Make Graves>, <artist - Huggy Bear>, <artist - Bratmobile>, <artist - Team Dresch>]
        >>> 
        """
        buckets = buckets or []
        kwargs = {}
        if max_familiarity:
            kwargs['max_familiarity'] = max_familiarity
        if min_familiarity:
            kwargs['min_familiarity'] = min_familiarity
        if max_hotttnesss:
            kwargs['max_hotttnesss'] = max_hotttnesss
        if min_hotttnesss:
            kwargs['min_hotttnesss'] = min_hotttnesss
        if min_results:
            kwargs['min_results'] = min_results
        if buckets:
            kwargs['bucket'] = buckets
        if limit:
            kwargs['limit'] = 'true'
        if reverse:
            kwargs['reverse'] = 'true'
        
        if cache and ('similar' in self.cache) and results==15 and start==0 and (not kwargs):
            return [Artist(**util.fix(a)) for a in self.cache['similar']]
        else:
            response = self.get_attribute('similar', results=results, start=start, **kwargs)
            if results==15 and start==0 and (not kwargs):
                self.cache['similar'] = response['artists']
            return [Artist(**util.fix(a)) for a in response['artists']]
    
    similar = property(get_similar)    
    
    def get_songs(self, cache=True, results=15, start=0):
        """Get the songs associated with an artist
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
            
        Results:
            A list of Song objects; list contains additional attributes 'start' and 'total'
        
        Example:

        >>> a = artist.Artist('Strokes')
        >>> a.get_songs(results=5)
        [<song - Fear Of Sleep>, <song - Red Light>, <song - Ize Of The World>, <song - Evening Sun>, <song - Juicebox>]
        >>> 
        """

        if cache and ('songs' in self.cache) and results==15 and start==0:
            return self.cache['songs']
        else:
            response = self.get_attribute('songs', results=results, start=start)
            for s in response['songs']:
                s.update({'artist_id':self.id, 'artist_name':self.name})
            songs = [Song(**util.fix(s)) for s in response['songs']]
            if results==15 and start==0:
                self.cache['songs'] = ResultList(songs, 0, response['total'])
            return ResultList(songs, start, response['total'])
    
    songs = property(get_songs)

    def get_terms(self, sort='weight', cache=True):
        """Get the terms associated with an artist
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            sort (str): A string specifying the desired sorting type (weight or frequency)
            
        Results:
            A list of term document dicts
            
        Example:

        >>> a = artist.Artist('tom petty')
        >>> a.terms
        [{u'frequency': 1.0, u'name': u'heartland rock', u'weight': 1.0},
         {u'frequency': 0.88569401860168606,
          u'name': u'jam band',
          u'weight': 0.9116501862732439},
         {u'frequency': 0.9656145118557401,
          u'name': u'pop rock',
          u'weight': 0.89777934440040685},
         {u'frequency': 0.8414744288140491,
          u'name': u'southern rock',
          u'weight': 0.8698567153186606},
         {u'frequency': 0.9656145118557401,
          u'name': u'hard rock',
          u'weight': 0.85738022655218893},
         {u'frequency': 0.88569401860168606,
          u'name': u'singer-songwriter',
          u'weight': 0.77427243392312772},
         {u'frequency': 0.88569401860168606,
          u'name': u'rock',
          u'weight': 0.71158718989399083},
         {u'frequency': 0.60874110500110956,
          u'name': u'album rock',
          u'weight': 0.69758668733499629},
         {u'frequency': 0.74350792060935744,
          u'name': u'psychedelic',
          u'weight': 0.68457367494207944},
         {u'frequency': 0.77213698386292873,
          u'name': u'pop',
          u'weight': 0.65039556639337293},
         {u'frequency': 0.41747136183050298,
          u'name': u'bar band',
          u'weight': 0.54974975024767025}]
        >>> 

        """
        if cache and ('terms' in self.cache) and sort=='weight':
            return self.cache['terms']
        else:
            response = self.get_attribute('terms', sort=sort)
            if sort=='weight':
                self.cache['terms'] = response['terms']
            return response['terms']
    
    terms = property(get_terms)
    
    def get_urls(self, cache=True):
        """Get the urls for an artist
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
        Results:
            A url document dict
            
        Example:

        >>> a = artist.Artist('the unicorns')
        >>> a.get_urls()
        {u'amazon_url': u'http://www.amazon.com/gp/search?ie=UTF8&keywords=The Unicorns&tag=httpechonecom-20&index=music',
         u'aolmusic_url': u'http://music.aol.com/artist/the-unicorns',
         u'itunes_url': u'http://itunes.com/TheUnicorns',
         u'lastfm_url': u'http://www.last.fm/music/The+Unicorns',
         u'mb_url': u'http://musicbrainz.org/artist/603c5f9f-492a-4f21-9d6f-1642a5dbea2d.html',
         u'myspace_url': u'http://www.myspace.com/iwasbornunicorn'}
        >>> 

        """
        if not (cache and ('urls' in self.cache)):
            response = self.get_attribute('urls')
            self.cache['urls'] = response['urls']
        return self.cache['urls']
    
    urls = property(get_urls)    
    
    def get_video(self, results=15, start=0, cache=True):
        """Get a list of video documents found on the web related to an artist
        
        Args:
        
        Kwargs:
            cache (bool): A boolean indicating whether or not the cached value should be used (if available). Defaults to True.
            
            results (int): An integer number of results to return
            
            start (int): An integer starting value for the result set
        
        Returns:
            A list of video document dicts; list contains additional attributes 'start' and 'total'
            
        Example:

        >>> a = artist.Artist('the vapors')
        >>> a.get_video(results=1, start=2)
        [{u'date_found': u'2009-12-28T08:27:48',
          u'id': u'd02f9e6dc7904f70402d4676516286b9',
          u'image_url': u'http://i1.ytimg.com/vi/p6c0wOFL3Us/default.jpg',
          u'site': u'youtube',
          u'title': u'The Vapors-Turning Japanese (rectangular white vinyl promo)',
          u'url': u'http://youtube.com/watch?v=p6c0wOFL3Us'}]
        >>> 

        """
        if cache and ('video' in self.cache) and results==15 and start==0:
            return self.cache['video']
        else:
            response = self.get_attribute('video', results=results, start=start)
            if results==15 and start==0:
                self.cache['video'] = ResultList(response['video'], 0, response['total'])
            return ResultList(response['video'], start, response['total'])
    
    video = property(get_video)

def search(name=None, description=None, results=15, buckets=None, limit=False, \
            fuzzy_match=False, sort=None, max_familiarity=None, min_familiarity=None, \
            max_hotttnesss=None, min_hotttnesss=None):
    """Search for artists by name, description, or constraint.
    
    Args:
    
    Kwargs:
        name (str): the name of an artist
        
        description (str): A string describing the artist
        
        results (int): An integer number of results to return
        
        buckets (list): A list of strings specifying which buckets to retrieve
        
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
        fuzzy_match (bool): A boolean indicating whether or not to search for similar sounding matches (only works with name)
        
        max_familiarity (float): A float specifying the max familiarity of artists to search for
        
        min_familiarity (float): A float specifying the min familiarity of artists to search for
        
        max_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
        
        min_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
    
    Returns:
        A list of Artist objects
    
    Example:
    
    >>> results = artist.search(name='t-pain')
    >>> results
    [<artist - T-Pain>, <artist - T-Pain & Lil Wayne>, <artist - T Pain & 2 Pistols>, <artist - Roscoe Dash & T-Pain>, <artist - Tony Moxberg & T-Pain>, <artist - Flo-Rida (feat. T-Pain)>, <artist - Shortyo/Too Short/T-Pain>]
    >>> 

    """
    buckets = buckets or []
    kwargs = {}
    if name:
        kwargs['name'] = name
    if description:
        kwargs['description'] = description
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    if fuzzy_match:
        kwargs['fuzzy_match'] = 'true'
    if max_familiarity is not None:
        kwargs['max_familiarity'] = max_familiarity
    if min_familiarity is not None:
        kwargs['min_familiarity'] = min_familiarity
    if max_hotttnesss is not None:
        kwargs['max_hotttnesss'] = max_hotttnesss
    if min_hotttnesss is not None:
        kwargs['min_hotttnesss'] = min_hotttnesss
    if sort:
        kwargs['sort'] = sort
    
    """Search for artists"""
    result = util.callm("%s/%s" % ('artist', 'search'), kwargs)
    return [Artist(**util.fix(a_dict)) for a_dict in result['response']['artists']]

def top_hottt(start=0, results=15, buckets = None, limit=False):
    """Get the top hotttest artists, according to The Echo Nest
    
    Args:
    
    Kwargs:
        results (int): An integer number of results to return
        
        start (int): An integer starting value for the result set
        
        buckets (list): A list of strings specifying which buckets to retrieve
        
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
    Returns:
        A list of hottt Artist objects

    Example:

    >>> hot_stuff = artist.top_hottt()
    >>> hot_stuff
    [<artist - Deerhunter>, <artist - Sufjan Stevens>, <artist - Belle and Sebastian>, <artist - Glee Cast>, <artist - Linkin Park>, <artist - Neil Young>, <artist - Jimmy Eat World>, <artist - Kanye West>, <artist - Katy Perry>, <artist - Bruno Mars>, <artist - Lady Gaga>, <artist - Rihanna>, <artist - Lil Wayne>, <artist - Jason Mraz>, <artist - Green Day>]
    >>> 

    """
    buckets = buckets or []
    kwargs = {}
    if start:
        kwargs['start'] = start
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    """Get top hottt artists"""
    result = util.callm("%s/%s" % ('artist', 'top_hottt'), kwargs)
    return [Artist(**util.fix(a_dict)) for a_dict in result['response']['artists']]    


def top_terms(results=15):
    """Get a list of the top overall terms
        
    Args:
    
    Kwargs:
        results (int): An integer number of results to return
        
    Returns:
        A list of term document dicts
    
    Example:
    
    >>> terms = artist.top_terms(results=5)
    >>> terms
    [{u'frequency': 1.0, u'name': u'rock'},
     {u'frequency': 0.99054710039307992, u'name': u'electronic'},
     {u'frequency': 0.96131624654034398, u'name': u'hip hop'},
     {u'frequency': 0.94358477322411127, u'name': u'jazz'},
     {u'frequency': 0.94023302416455468, u'name': u'pop rock'}]
    >>> 
    """
    
    kwargs = {}
    if results:
        kwargs['results'] = results
    
    """Get top terms"""
    result = util.callm("%s/%s" % ('artist', 'top_terms'), kwargs)
    return result['response']['terms']


def similar(names=None, ids=None, start=0, results=15, buckets=None, limit=False, max_familiarity=None, min_familiarity=None,
            max_hotttnesss=None, min_hotttnesss=None):
    """Return similar artists to this one
    
    Args:
    
    Kwargs:
        ids (str/list): An artist id or list of ids
        
        names (str/list): An artist name or list of names
        
        results (int): An integer number of results to return
        
        buckets (list): A list of strings specifying which buckets to retrieve
        
        limit (bool): A boolean indicating whether or not to limit the results to one of the id spaces specified in buckets
        
        start (int): An integer starting value for the result set
        
        max_familiarity (float): A float specifying the max familiarity of artists to search for
        
        min_familiarity (float): A float specifying the min familiarity of artists to search for
        
        max_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
        
        min_hotttnesss (float): A float specifying the max hotttnesss of artists to search for
    
    Returns:
        A list of similar Artist objects
    
    Example:

    >>> some_dudes = [artist.Artist('weezer'), artist.Artist('radiohead')]
    >>> some_dudes
    [<artist - Weezer>, <artist - Radiohead>]
    >>> sims = artist.similar(ids=[art.id for art in some_dudes], results=5)
    >>> sims
    [<artist - The Smashing Pumpkins>, <artist - Biffy Clyro>, <artist - Death Cab for Cutie>, <artist - Jimmy Eat World>, <artist - Nerf Herder>]
    >>> 

    """
    
    buckets = buckets or []
    kwargs = {}

    if ids:
        if not isinstance(ids, list):
            ids = [ids]
        kwargs['id'] = ids
    if names:
        if not isinstance(names, list):
            names = [names]
        kwargs['name'] = names
    if max_familiarity is not None:
        kwargs['max_familiarity'] = max_familiarity
    if min_familiarity is not None:
        kwargs['min_familiarity'] = min_familiarity
    if max_hotttnesss is not None:
        kwargs['max_hotttnesss'] = max_hotttnesss
    if min_hotttnesss is not None:
        kwargs['min_hotttnesss'] = min_hotttnesss
    if start:
        kwargs['start'] = start
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'

    result = util.callm("%s/%s" % ('artist', 'similar'), kwargs)
    return [Artist(**util.fix(a_dict)) for a_dict in result['response']['artists']]    

