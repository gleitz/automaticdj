# -*- coding: utf-8 -*-
#
# Name: face.com Python API client library
# Description: face.com REST API Python client library.
#
# For more information about the API and the return values,
# visit the official documentation at http://developers.face.com/docs/api/.
#
# Author: Tomaž Muraus (http://www.tomaz-muraus.info)
# License: GPL (http://www.gnu.org/licenses/gpl.html)
# Version: 1.0

import urllib
import urllib2
import simplejson as json
import os.path

API_URL	= 'http://api.face.com'

class FaceClient(object):
	def __init__(self, api_key = None, api_secret = None):
		if not api_key or not api_secret:
			raise AttributeError('Missing api_key or api_secret argument')

		self.api_key 				= api_key
		self.api_secret 			= api_secret
		self.format 				= 'json'

		self.twitter_credentials	= None
		self.facebook_credentials 	= None

	def set_twitter_user_credentials(self, user = None, password = None):
		if not user or not password:
			raise AttributeError('Missing Twitter username or password')

		self.twitter_credentials = {'twitter_user': user,
									'twitter_password': password}

	def set_twitter_oauth_credentials(self, user = None, secret = None, token = None):
		if not user or not secret or not token:
			raise AttributeError('Missing one of the required arguments')

		self.twitter_credentials = {'twitter_oauth_user': user,
									'twitter_oauth_secret': secret,
									'twitter_oauth_token': token}

	def set_facebook_credentials(self, user = None, session = None):
		if not user or not session:
			raise AttributeError('Missing Facebook user or session argument')

		self.facebook_credentials = {'fb_user': user,
									'fb_session': session}

	### Recognition engine methods ###
	def faces_detect(self, urls = None, file = None, aggressive=False):
		"""
		Returns tags for detected faces in one or more photos, with geometric information
		of the tag, eyes, nose and mouth, as well as the gender, glasses, and smiling attributes.

		http://developers.face.com/docs/api/faces-detect/
		"""
		if not urls and not file:
			raise AttributeError('Missing URLs/filename argument')

		if file:
			# Check if the file exists
			if not os.path.exists(file):
				raise IOError('File %s does not exist' % (file))

			data = {'file': file}
		else:
			data = {'urls': urls}

		if aggressive:
			data['detector'] = 'Aggressive'

		response = self.send_request('faces/detect', data)
		return response

	def faces_status(self, uids = None, namespace = None):
		"""
		Reports training set status for the specified UIDs.

		http://developers.face.com/docs/api/faces-status/
		"""
		if not uids:
			raise AttributeError('Missing user IDs')

		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uids)

		data = {'uids': uids}
		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, namespace = namespace)

		response = self.send_request('faces/status', data)
		return response

	def faces_recognize(self, uids = None, urls = None, file = None, train = None, \
						namespace = None, aggressive = None):
		"""
		Attempts to detect and recognize one or more user IDs' faces, in one or more photos.
		For each detected face, the face.com engine will return the most likely user IDs,
		or empty result for unrecognized faces. In addition, each tag includes a threshold
		score - any score below this number is considered a low-probability hit.

		http://developers.face.com/docs/api/faces-recognize/
		"""
		if not uids or (not urls and not file):
			raise AttributeError('Missing required arguments')

		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uids)

		data = {'uids': uids}

		if file:
			# Check if the file exists
			if not os.path.exists(file):
				raise IOError('File %s does not exist' % (file))

			data.update({'file': file})
		else:
			data.update({'urls': urls})

		if aggressive:
			data['detector'] = 'Aggressive'

		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, train = train, namespace = namespace)

		response = self.send_request('faces/recognize', data)
		return response

	def faces_train(self, uids = None, namespace = None, callback = None):
		"""
		Calls the training procedure for the specified UIDs, and reports back changes.

		http://developers.face.com/docs/api/faces-train/
		"""
		if not uids:
			raise AttributeError('Missing user IDs')

		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uids)

		data = {'uids': uids}
		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, namespace = namespace, callback = callback)

		response = self.send_request('faces/train', data)
		return response

	### Methods for managing face tags ###
	def tags_get(self, uids = None, urls = None, pids = None, order = 'recent', \
				limit = 5, together = False, filter = None, namespace = None):
		"""
		Returns saved tags in one or more photos, or for the specified User ID(s).
		This method also accepts multiple filters for finding tags corresponding to
		a more specific criteria such as front-facing, recent, or where two or more
		users appear together in same photos.

		http://developers.face.com/docs/api/tags-get/
		"""
		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uids)

		data = {'uids': uids,
				'urls': urls,
				'together': together,
				'limit': limit}
		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, pids = pids, filter = filter, \
										namespace = namespace)

		response = self.send_request('tags/get', data)
		return response

	def tags_add(self, url = None, x = None, y = None, width = None, uid = None, \
				tagger_id = None, label = None, password = None):
		"""
		Add a (manual) face tag to a photo. Use this method to add face tags where
		those were not detected for completeness of your service.

		http://developers.face.com/docs/api/tags-add/
		"""
		if not url or not x or not y or not width or not uid or not tagger_id:
			raise AttributeError('Missing one of the required arguments')

		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uid)

		data = {'url': url,
				'x': x,
				'y': y,
				'width': width,
				'uid': uid,
				'tagger_id': tagger_id}
		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, label = label, password = password)

		response = self.send_request('tags/add', data)
		return response

	def tags_save(self, tids = None, uid = None, tagger_id = None, label = None, \
				password = None):
		"""
		Saves a face tag. Use this method to save tags for training the face.com
		index, or for future use of the faces.detect and tags.get methods.

		http://developers.face.com/docs/api/tags-save/
		"""
		if not tids or not uid:
			raise AttributeError('Missing required argument')

		(facebook_uids, twitter_uids) = self.__check_user_auth_credentials(uid)

		data = {'tids': tids,
				'uid': uid}
		self.__append_user_auth_data(data, facebook_uids, twitter_uids)
		self.__append_optional_arguments(data, tagger_id = tagger_id, label = label, \
										password = password)

		response = self.send_request('tags/save', data)
		return response

	def tags_remove(self, tids = None, password = None):
		"""
		Remove a previously saved face tag from a photo.

		http://developers.face.com/docs/api/tags-remove/
		"""
		if not tids:
			raise AttributeError('Missing tag IDs')

		data = {'tids': tids}

		response = self.send_request('tags/remove', data)
		return response

	### Account management methods ###
	def account_limits(self):
		"""
		Returns current rate limits for the account represented by the passed API key and Secret.

		http://developers.face.com/docs/api/account-limits/
		"""
		response = self.send_request('account/limits')
		return response['usage']

	def account_users(self, namespaces = None):
		"""
		Returns current rate limits for the account represented by the passed API key and Secret.

		http://developers.face.com/docs/api/account-limits/
		"""
		if not namespaces:
			raise AttributeError('Missing namespaces argument')

		response = self.send_request('account/users', {'namespaces': namespaces})

		return response

	def __check_user_auth_credentials(self, uids):
		# Check if needed credentials are provided
		facebook_uids = [uid for uid in uids.split(',') \
						if uid.find('@facebook.com') != -1]
		twitter_uids = [uid for uid in uids.split(',') \
						if uid.find('@twitter.com') != -1]

		if facebook_uids and not self.facebook_credentials:
			raise AttributeError('You need to set Facebook credentials to perform action on Facebook users')

		if twitter_uids and not self.twitter_credentials:
			raise AttributeError('You need to set Twitter credentials to perform action on Twitter users')

		return (facebook_uids, twitter_uids)

	def __append_user_auth_data(self, data, facebook_uids, twitter_uids):
		if facebook_uids:
			data.update({'user_auth': 'fb_user:%s,fb_oauth_token:%s' % (self.facebook_credentials['fb_user'],
						 self.facebook_credentials['fb_session'])})

		if twitter_uids:
			# If both user/password and OAuth credentials are provided, use
			# OAuth as default
			if self.twitter_credentials.get('twitter_oauth_user', None):
				data.update({'user_auth': 'twitter_oauth_user:%s,twitter_oauth_secret:%s,twitter_oauth_token:%s' %
							(self.twitter_credentials['twitter_oauth_user'], self.twitter_credentials['twitter_oauth_secret'], \
							self.twitter_credentials['twitter_oauth_token'])})
			else:
				data.update({'user_auth': 'twitter_user:%s,twitter_password:%s' % (self.twitter_credentials['twitter_user'],
							 self.twitter_credentials['twitter_password'])})

	def __append_optional_arguments(self, data, **kwargs):
		for key, value in kwargs.iteritems():
			if value:
				data.update({key: value})

	def send_request(self, method = None, parameters = None):
		url = '%s/%s' % (API_URL, method)

		data = {'api_key': self.api_key,
				'api_secret': self.api_secret,
				'format': self.format}

		if parameters:
			data.update(parameters)
		# raise Exception(url, data)
		# Local file is provided, use multi-part form
		if 'file' in parameters:
			from multipart import Multipart
			form = Multipart()

			for key, value in data.iteritems():

				if key == 'file':
					file = open(value, 'r')
					# with open(value, 'r') as file:
					form.file(os.path.basename(key), os.path.basename(key), file.read())
				else:
					form.field(key, value)

			(content_type, post_data) = form.get()
			headers = {'Content-Type': content_type}
		else:
			post_data = urllib.urlencode(data)
			headers = {}

		request = urllib2.Request(url, headers = headers, data = post_data)
		response = urllib2.urlopen(request)
		response = response.read()
		response_data = json.loads(response)

		if 'status' in response_data and \
			response_data['status'] == 'failure':
			raise FaceError(response_data['error_code'], response_data['error_message'])

		return response_data

class FaceError(Exception):
	def __init__(self, error_code, error_message):
		self.error_code = error_code
		self.error_message = error_message

	def __str__(self):
		return '%s (%d)' % (self.error_message, self.error_code)
