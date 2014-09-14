import cookielib, urllib, urllib2
import subprocess
import HTMLParser
import os, re, sys, time
import xbmc, xbmcgui, xbmcplugin
from xbmcaddon import Addon
from PyQt4 import QtCore, QtGui
from resources.lib.btsport_login import BtSportLogin

__plugin__ = "BTSportXBMC"
__authors__ = "hirodotp"
__credits__ = "hirodotp"

__settings__ = Addon( id="plugin.video.btsportxbmc" )

class Main:
	def __init__(self):
		self._path = sys.argv[0]
		self._handle = int(sys.argv[1])
		self._get_settings()
		self.parser = HTMLParser.HTMLParser()

		param = sys.argv[2]
		if param:
			param = param[1:]
			try:
				movie = param.split('movie=').pop(1)
			except:
				movie = None

			try:
				category = param.split('category=').pop(1)
			except:
				category = None

			if movie:
				movie = urllib2.unquote(movie)
				scraper = NetflixbmcScraper()
				scraper.SignIn(self.settings['email'], self.settings['password'])
				cookies = scraper.GetCookies()

				home = os.getenv("HOME")
				cmd = os.path.abspath("%s/.xbmc/addons/plugin.video.netflixbmc/resources/lib/pipelight.py" % (home))

				args = [cmd, self.settings['pipelightName'], self.settings['pipelightDirectory'], self.settings['mozillaDirectory'], self.settings['gpuAccel'], movie]
				for cookie in cookies:
					args.append(cookie[0])
					args.append(cookie[1])

				subprocess.call(args)
			elif category:
				category = urllib2.unquote(category)
				try:
					genre = category.split("//").pop(1)
					if genre:
						category = category.split("//").pop(0)
				except:
					genre = None
					
				if category == 'instant':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetMyList()
					self.DisplayMyList(mylist)
				elif category == 'new':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetNewReleaseList()
					self.DisplayMyList(mylist)
				elif category == 'genre':
					try:
						genre = genre.split("//").pop(0)
					except:
						genre = None

					if genre is None:
						self.DisplayGenres('genre', CAT_GENRES)
					else:
						scraper = NetflixbmcScraper()
						scraper.SignIn(self.settings['email'], self.settings['password'])
						mylist = scraper.GetGenreList(GENRE_ID_MAP[genre], self.settings['maxTitles'])
						self.DisplayMyList(mylist)
				elif category == 'hd':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetHDReleaseList(self.settings['maxTitles'])
					self.DisplayMyList(mylist)
				elif category == 'recent':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetRecentReleaseList()
					self.DisplayMyList(mylist)
				elif category == 'kids':
					try:
						genre = genre.split("//").pop(0)
					except:
						genre = None

					if genre is None:
						self.DisplayGenres('kids', KID_GENRES)
					else:
						scraper = NetflixbmcScraper()
						scraper.SignIn(self.settings['email'], self.settings['password'])
						mylist = scraper.GetGenreList(KID_ID_MAP[genre], self.settings['maxTitles'], True)
						self.DisplayMyList(mylist)
		else:
			self.DisplayTopCategories()

	def DisplayMyList(self, mylist):
		for item in mylist:
			listitem = xbmcgui.ListItem(self.parser.unescape(item['title']), iconImage=item['boxart'], thumbnailImage=item['boxart'])
			movie = urllib.urlencode({'movie': item['movie']})
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?%s" % (self._path, movie), listitem=listitem, isFolder=False) 
		xbmcplugin.endOfDirectory(handle=self._handle, succeeded=True, cacheToDisc=False)

	def DisplayTopCategories(self):
		for item in TOP_CATEGORIES:
			listitem = xbmcgui.ListItem(self.parser.unescape(item['title']))
			lnk = item['link']
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?category=%s" % (self._path, lnk), listitem=listitem, isFolder=True) 
		xbmcplugin.endOfDirectory( handle=self._handle, succeeded=True, cacheToDisc=False )
			
	def DisplayGenres(self, category, genres):
		for item in genres: 
			listitem = xbmcgui.ListItem(self.parser.unescape(item['title']))
			lnk = item['link']
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?category=%s//%s" % (self._path, category, lnk), listitem=listitem, isFolder=True) 
		xbmcplugin.endOfDirectory( handle=self._handle, succeeded=True, cacheToDisc=False )

	def _get_settings( self ):
		# get the users preference settings
		self.settings = {}
		self.settings["email"] = __settings__.getSetting("email")
		self.settings["password"] = __settings__.getSetting("password")
		self.settings["maxTitles"] = int(__settings__.getSetting("maxTitles"))
		self.settings["gpuAccel"] = __settings__.getSetting("gpu")
		self.settings["pipelightName"] = __settings__.getSetting("pipelightName")
		self.settings["pipelightDirectory"] = __settings__.getSetting("pipelightDirectory")
		self.settings["mozillaDirectory"] = __settings__.getSetting("mozillaDirectory")

if __name__ == "__main__":
	import resources.lib.netflixbmc as plugin
	Main()
