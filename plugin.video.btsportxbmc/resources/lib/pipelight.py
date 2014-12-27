#!/usr/bin/env python
import sys
import os
import tempfile
import shutil
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import gtk
from pymouse import PyMouse
from time import sleep


def pixel_at(x, y):
    rw = gtk.gdk.get_default_root_window()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
    pixbuf = pixbuf.get_from_drawable(rw, rw.get_colormap(), x, y, 0, 0, 1, 1)
    return tuple(pixbuf.pixel_array[0, 0])


def screen_geometry():
    screen = gtk.Window().get_screen()

    # collect data about each monitor
    monitors = []
    nmons = screen.get_n_monitors()
    print "there are %d monitors" % nmons
    for m in range(nmons):
        mg = screen.get_monitor_geometry(m)
        monitors.append(mg)

    curmon = screen.get_monitor_at_window(screen.get_active_window())
    return monitors[curmon] # x, y, width, height


class PipelightMainWindow(QtGui.QMainWindow):
    def __init__(self, page, cookies=[]):
        QtGui.QMainWindow.__init__(self)
        self.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(0, 0, 0).name())

        self.cookies = cookies

        self.container = X11Container()
        self.container.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(self.container)
        self.setCentralWidget(self.container)
        self.setFocus(True)

        print "attempting to embed in {}".format(self.container.winId())
        os.putenv("PIPELIGHT_X11WINDOW", str(self.container.winId()))

        self.screen_geometry = screen_geometry()
        
        self.is_embedded = False
        self.browser = None
        self.browser_page = page
        self.loadBrowser()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def loadBrowser(self):
        self.browser = Browser(self.browser_page, self.cookies)

        timer = QtCore.QTimer()
        timer.singleShot(20000, self.checkIfEmbedded)

        self.timer_check_loaded = QtCore.QTimer(self)
        self.connect(self.timer_check_loaded, QtCore.SIGNAL("timeout()"), self.check_loaded)
        self.timer_check_loaded.start(1000)

    def checkIfEmbedded(self):
        if not self.is_embedded:
            print "Timeout reached and no Silverlight application embedded yet!"
            self.close()
            sys.exit(1)

    def get_play_coords(self):
        """
        Calculate the position of the yellow play arrow based upon screen geometry. On a 1080p
        screen with 1 monitor, the arrow is at 930, 541
        """
        x, y, width, height = self.screen_geometry
        arrow_x = int(round(width * 930.0/1920.0))
        arrow_y = int(round(height * 541.0/1080.0))
        return x + arrow_x, y + arrow_y

    def check_loaded(self):
        """
        This function checks if BTSport has loaded by checking pixel colours.
        """

        # Calculate the position of the yellow play arrow based upon screen geometry. On a 1080p
        # screen with 1 monitor, the arrow is at 930, 541
        colour = pixel_at(*self.get_play_coords())
        print colour
        if colour == (252, 225, 20):
            print 'loaded!'
            self.click_play()
            self.timer_check_loaded.stop()

    def click_play(self):
        play_x, play_y = self.get_play_coords()
        m = PyMouse()
        m.click(play_x, play_y, 1)

    def close(self):
        os.unsetenv("PIPELIGHT_X11WINDOW")

        # Set to empty string to let Silverlight unload the page properly
        if self.browser is not None:
            self.browser.setHtml(QtCore.QString(""))
            self.browser = None

            timer = QtCore.QTimer()
            timer.singleShot(100, self.close)
            return

        QtGui.QMainWindow.close(self)


class X11Container(QtGui.QX11EmbedContainer):
    def __init__(self):
        QtGui.QX11EmbedContainer.__init__(self)
        QtCore.QObject.connect(self, QtCore.SIGNAL('clientIsEmbedded()'), self.clientIsEmbedded)
        QtCore.QObject.connect(self, QtCore.SIGNAL('clientClose()'), self.clientClose)

    def focusInEvent(self, event):
        print 'Got focus'

    def focusOutEvent(self, event):
        print 'Lost focus'

    def keyPressEvent(self, event):
        print 'key pressed'
        self.window().keyPressEvent(event)

    def clientIsEmbedded(self):
        print "embedded"
        self.window().is_embedded = True

    def clientClose(self):
        print 'close'
        self.window().close()


class WebPage(QtWebKit.QWebPage):
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1"


class Browser(QtWebKit.QWebView):
    def __init__(self, url, cookies=[]):
        QtWebKit.QWebView.__init__(self)
        self.resize(800, 600)

        print "loading {}".format(url)

        # setup cookies
        cookieList = []
        for cookie in cookies:
            cookieList.append(QtNetwork.QNetworkCookie(cookie[0], cookie[1]))
        cookieJar = QtNetwork.QNetworkCookieJar()
        cookieJar.setCookiesFromUrl(cookieList, QtCore.QUrl(url))
        nmanager = QtNetwork.QNetworkAccessManager()
        nmanager.setCookieJar(cookieJar)

        # create webpage
        page = WebPage()
        page.setNetworkAccessManager(nmanager)
        self.setPage(page)

        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        QtCore.QObject.connect(self, QtCore.SIGNAL('loadFinished(bool)'), self.loadFinished)
        self.load(QtCore.QUrl(url))

    def loadFinished(self, ok):
        pass


class Pipelight(object):

    def __init__(self, pipelightName, pipelightDirectory, mozillaDirectory):
        self.pipelightName = pipelightName
        self.pipelightDirectory = pipelightDirectory
        self.mozillaDirectory = mozillaDirectory

        if not os.path.exists("%s/%s" % (self.pipelightDirectory, self.pipelightName)):
            print "It looks like pipelight is not installed! Unable to find '%s'." % self.pipelightName
            sys.exit(1)

        self.enabled_systemwide = os.path.exists("%s/%s" % (self.mozillaDirectory, self.pipelightName))

    def play(self, page, cookies=[]):
        # Pipelight not enabled systemwide, create a temporary plugin dir
        if not self.enabled_systemwide:
            print "not enabled system wide!"

        # Show the Silverlight plugin in a QtGui window
        app = QtGui.QApplication([])  # (sys.argv) ?
        app.setAttribute(QtCore.Qt.AA_NativeWindows, True)
        mainWindow = PipelightMainWindow(page, cookies)
        mainWindow.showFullScreen()
        app.exec_()

if __name__ == "__main__":
    print sys.argv
    sys.argv.pop(0)
    pipelightName = sys.argv.pop(0)
    pipelightDirectory = sys.argv.pop(0)
    mozillaDirectory = sys.argv.pop(0)
    gpuAccel = sys.argv.pop(0)
    url = sys.argv.pop(0)

    # force gpu acceleration if specified to
    if gpuAccel == "true":
        os.putenv("PIPELIGHT_GPUACCELERATION", "1")

    cookies = []
    c = []
    i = True
    for cookie in sys.argv:
        c.append(cookie)
        if i:
            i = False
        else:
            i = True
            cookies.append(c)
            c = []

    player = Pipelight(pipelightName, pipelightDirectory, mozillaDirectory)
    player.play(url, cookies)
