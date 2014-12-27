import cookielib
import urllib
import urllib2
import subprocess
import HTMLParser
import os
import re
import sys
import time
import xbmc
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from PyQt4 import QtCore, QtGui
from resources.lib.btsport_login import BtSportLogin
from collections import OrderedDict


__plugin__ = "BTSportXBMC"
__authors__ = "jackandrews"
__credits__ = "jackandrews"

__settings__ = Addon(id="plugin.video.btsportxbmc")

CHANNELS = ({'name': 'BT Sport 1', 'icon': 'bt-sport-1.png', 'url': 'http://sport.bt.com/btsportplayer/bt-sport-1-01363810201090'},
    {'name': 'BT Sport 2', 'icon': 'bt-sport-2.png', 'url': 'http://sport.bt.com/btsportplayer/bt-sport-2-01363810201819'},
    {'name': 'ESPN', 'icon': 'espn.png', 'url': 'http://sport.bt.com/btsportplayer/espn-01363810201883'})


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
                self.play_channel(channel)
            except:
                ValueError('Unknown parameter')
        else:
            self.display_channels()

    def play_channel(self, channel):
        home = os.getenv("HOME")
        cmd = os.path.abspath("%s/.xbmc/addons/plugin.video.btsportxbmc/resources/lib/pipelight.py" % home)

        args = [cmd, self.settings['pipelightName'], self.settings['pipelightDirectory'],
                self.settings['mozillaDirectory'], self.settings['gpuAccel'], channel]

        print "logging in"
        login = BtSportLogin(self.settings['email'], self.settings['password'])
        cookies = login.get_cookies()
        for cookie in cookies:
            args.append(cookie[0])
            args.append(cookie[1])

        print args

        subprocess.call(args)

    def display_channels(self):
        for channel in CHANNELS:
            list_item = xbmcgui.ListItem(channel['name'])
            list_item.setIconImage(xbmc.translatePath(os.path.join(__settings__.getAddonInfo('path'),'resources/icons/{}'.format(channel['icon']))))
            xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?channel=%s" % (self._path, channel['url']),
                                        listitem=list_item, isFolder=False)
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
    import resources.lib.btsport_login as plugin
    Main()
