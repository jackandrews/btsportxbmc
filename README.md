Overview
========

This is an attempt to get BT Sport running in XBMC on Linux using Pipelight.


How it Works
============

Using pipelight and PyQt4 to implement a standalone embedded pipelight viewer, you can now watch  
BT Sport in xbmc on Linux!


Prerequisites
=============

1. You need Linux to use this Addon.

2. You need to install pipelight.  For a tutorial on installing pipelight see  the website:
   http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
   Ensure you can view BT Sport in Firefox (Chrome no longer supports pipelight) before continuing.

3. You need to install PyQt4.  In ubuntu you can do this by running the 
   command "apt-get install python-qt4".


Gotchyas
========

You can close the pipelight window by sending an Escape key.

You need a window manager running.  If you're running xbmc in standalone mode
you'll need to have fluxbox or some other manager running.

People running compiz, emerald, etc. may experience issues with the player (try disabling these if they are running).

Don't forget to autohide your mouse with unclutter!


Thank You
=========

This is a quick and dirty fork from https://github.com/hirodotp/netflixbmc. Credit to him + slackner for the bulk of the work...
