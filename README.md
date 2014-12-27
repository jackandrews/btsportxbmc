Overview
========

This is an XBMC plugin to play BT Sport on XBMC using Pipelight.  It requires linux.

How it Works
============

PyQt4 is used to implement a standalone fullscreen Pipelight viewer for BT Sport.  It automatically logs in, waits for BT Sport to load, hits play and goes fullscreen.

Installation
============

1. You need to install Pipelight, enabling Silverlight 5.0 (5.1 is broken with BT Sport).  For a tutorial on installing pipelight see this website:
   http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
   Note: version 0.2.8 in the stable Pipelight repo contains a bug which breaks this plugin.  If the version in the stable repo is not > 0.2.8, please use the nightly repo instead.  Version 0.2.8~daily-201412150616 is tested and known to work.  If you have already installed Pipelight from the stable repo, please disable this repo, enable nightly, purge Pipelight and re-install.

2. Ensure you can view BT Sport in Firefox (Chrome no longer supports pipelight).

3. Install the following dependencies:
   "sudo apt-get install python-qt4 python-numpy python-xlib"
   "sudo easy_install PyUserInput"

4. Test the standalone BT Sport player:
   "vim plugin.video.btsportxbmc/resources/lib/test_pipelight.py" (enter your BT sport username and password here)
   "python plugin.video.btsportxbmc/resources/lib/test_pipelight.py" (check that you get BT Sport 1 playing)

5. Configure the XBMC plugin (enter username and password - otherwise default settings should be fine).

Gotchyas
========

You can close the pipelight window by sending an Escape key.

You need a window manager running.  If you're running xbmc in standalone mode you'll need to have fluxbox or some other manager running.

People running compiz, emerald, etc. may experience issues with the player (try disabling these if they are running).

Don't forget to autohide your mouse with unclutter!


Thank You
=========

This is a quick and dirty fork from https://github.com/hirodotp/netflixbmc. Credit to him + slackner for the bulk of the work...
