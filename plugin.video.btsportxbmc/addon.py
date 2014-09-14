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

CHANNELS = {
	'BT Sport 1': '',
	'BT Sport 2': '',
	'ESPN': ''
	}

class Main:
	def __init__(self):
		self._path = sys.argv[0]
		self._handle = int(sys.argv[1])
		self._get_settings()
		param = sys.argv[2]
		if param:
			param = param[1:]
			try:
				channel = param.split('channel=').pop(1)
			except:
				except ValueError('Unknown parameter')
			self.login = BtSportLogin(self.settings['email'],self.settings['password'])


			home = os.getenv("HOME")
			cmd = os.path.abspath("%s/.xbmc/addons/plugin.video.btsportxbmc/resources/lib/pipelight.py" % (home))

			args = [cmd, self.settings['pipelightName'], self.settings['pipelightDirectory'], self.settings['mozillaDirectory'], self.settings['gpuAccel'], channel]
		
			cookies = login.get_cookies()
			for cookie in cookies:
				args.append(cookie[0])
				args.append(cookie[1])
		else:
			display_channels()

	def display_channels(self):
		for channel in CHANNELS:
			listitem = xbmcgui.ListItem(self.parser.unescape(channel['title']))
			lnk = channel['link']
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?channel=%s" % (self._path, lnk), listitem=listitem, isFolder=False) 
		xbmcplugin.endOfDirectory(handle=self._handle, succeeded=True, cacheToDisc=False)

	def _get_settings(self):
		# get the users preference settings
		self.settings = {}
		self.settings["email"] = __settings__.getSetting("email")
		self.settings["password"] = __settings__.getSetting("password")
		self.settings["gpuAccel"] = __settings__.getSetting("gpu")
		self.settings["pipelightName"] = __settings__.getSetting("pipelightName")
		self.settings["pipelightDirectory"] = __settings__.getSetting("pipelightDirectory")
		self.settings["mozillaDirectory"] = __settings__.getSetting("mozillaDirectory")

if __name__ == "__main__":
	import resources.lib.btsportxbmc as plugin
	Main()
