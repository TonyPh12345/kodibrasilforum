# -*- coding: utf-8 -*-
#
import xbmcaddon
import logging
from trakt import Trakt, ClientError, ServerError
from trakt.objects import Movie, Show
from utilities import getSetting, findMovieMatchInList, findEpisodeMatchInList, notification, getString, createError

# read settings
__addon__ = xbmcaddon.Addon('script.trakt')
__addonversion__ = __addon__.getAddonInfo('version')

logger = logging.getLogger(__name__)

class traktAPI(object):
	__apikey = "d4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868"
	__token = ""
	__username = ""
	__password = ""

	def __init__(self):
		logger.debug("Initializing.")

		# Get user login data
		self.__username = getSetting('username')
		self.__password = getSetting('password')

		# Configure
		Trakt.configuration.defaults.client(
			id=self.__apikey
		)

		if not self.__token:
			self.getToken()

	# helper for onSettingsChanged
	def updateSettings(self):

		_username = getSetting('username')
		_password = getSetting('password')

		updated = False
		if self.__username != _username:
			self.__username = _username
			updated = True

		if self.__password != _password:
			self.__password = _password
			updated = True

		if updated:
			self.getToken()

	def getToken(self):
		if not self.__username and not self.__password:
			notification('Trakt', getString(32021)) #Username and password error
		elif not self.__password:
			notification('Trakt', getString(32022)) #Password error
		else:
			# Attempt authentication (retrieve new token)
			with Trakt.configuration.http(retry=True):
				try:
					auth = Trakt['auth'].login(getSetting('username'), getSetting('password'))
					if auth:
						self.__token = auth
					else:
						logger.debug("Authentication Failure")
						notification('Trakt', getString(32025))
				except Exception as ex:
					message = createError(ex)
					logger.fatal(message)
					logger.debug("Cannot connect to server")
					notification('Trakt', getString(32023))



	def scrobbleEpisode(self, show, episode, percent, status):
		result = None

		with Trakt.configuration.auth(self.__username, self.__token):
			if status == 'start':
				with Trakt.configuration.http(retry=True):
					result =Trakt['scrobble'].start(
						show=show,
						episode=episode,
						progress=percent)
			elif status == 'pause':
				with Trakt.configuration.http(retry=True):
					result = Trakt['scrobble'].pause(
						show=show,
						episode=episode,
						progress=percent)
			elif status == 'stop':
				#don't retry on stop, this will cause multiple scrobbles
				result = Trakt['scrobble'].stop(
					show=show,
					episode=episode,
					progress=percent)
			else:
					logger.debug("scrobble() Bad scrobble status")
		return result


	def scrobbleMovie(self, movie, percent, status):
		result = None

		with Trakt.configuration.auth(self.__username, self.__token):
			if status == 'start':
				with Trakt.configuration.http(retry=True):
					result = Trakt['scrobble'].start(
						movie=movie,
						progress=percent)
			elif status == 'pause':
				with Trakt.configuration.http(retry=True):
					result = Trakt['scrobble'].pause(
						movie=movie,
						progress=percent)
			elif status == 'stop':
				#don't retry on stop, this will cause multiple scrobbles
				result = Trakt['scrobble'].stop(
					movie=movie,
					progress=percent)
			else:
				logger.debug("scrobble() Bad scrobble status")
		return result

	def getShowsCollected(self, shows):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True, timeout=90):
				Trakt['sync/collection'].shows(shows, exceptions=True)
		return shows

	def getMoviesCollected(self, movies):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True, timeout=90):
				Trakt['sync/collection'].movies(movies, exceptions=True)
		return movies


	def getShowsWatched(self, shows):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True, timeout=90):
				Trakt['sync/watched'].shows(shows, exceptions=True)
		return shows

	def getMoviesWatched(self, movies):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True, timeout=90):
				Trakt['sync/watched'].movies(movies, exceptions=True)
		return movies

	def addToCollection(self, mediaObject):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				result = Trakt['sync/collection'].add(mediaObject)
		return result

	def removeFromCollection(self, mediaObject):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				result = Trakt['sync/collection'].remove(mediaObject)
		return result

	def addToHistory(self, mediaObject):
		with Trakt.configuration.auth(self.__username, self.__token):
			#don't rtry this call it may cause multiple watches
			result = Trakt['sync/history'].add(mediaObject)
		return result

	def getEpisodeRatingForUser(self, tvdbId, season, episode):
		ratings = {}
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				Trakt['sync/ratings'].episodes(ratings)
		return findEpisodeMatchInList(tvdbId, season, episode, ratings)

	def getMovieRatingForUser(self, imdbId):
		ratings = {}
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				Trakt['sync/ratings'].movies(ratings)
		return findMovieMatchInList(imdbId, ratings)

	# Send a rating to Trakt as mediaObject so we can add the rating
	def addRating(self, mediaObject):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				result = Trakt['sync/ratings'].add(mediaObject)
		return result

	# Send a rating to Trakt as mediaObject so we can remove the rating
	def removeRating(self, mediaObject):
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				result = Trakt['sync/ratings'].remove(mediaObject)
		return result

	def getMoviePlaybackProgress(self):
		progressMovies = []

		# Fetch playback
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				playback = Trakt['sync/playback'].movie(exceptions=True)

				for key, item in playback.items():
					if type(item) is Movie:
						progressMovies.append(item)

		return progressMovies

	def getEpisodePlaybackProgress(self):
		progressShows = []

		# Fetch playback
		with Trakt.configuration.auth(self.__username, self.__token):
			with Trakt.configuration.http(retry=True):
				playback = Trakt['sync/playback'].shows(exceptions=True)

				for key, item in playback.items():
					if type(item) is Show:
						progressShows.append(item)

		return progressShows
