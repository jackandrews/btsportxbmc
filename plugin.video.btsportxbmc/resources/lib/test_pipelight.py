import os
import subprocess
from btsport_login import BtSportLogin

# Enter your username and password here and then run the script. BT Sport 2 should display in fullscreen.
USERNAME = 'my_bt_sport_username'
PASSWORD = 'my_password'

if __name__ == "__main__":
    home = os.getenv("HOME")
    cmd = os.path.abspath("%s/.xbmc/addons/plugin.video.btsportxbmc/resources/lib/pipelight.py" % home)

    args = [cmd, "libpipelight-silverlight5.0.so", "/usr/lib/pipelight",
            "/usr/lib/mozilla/plugins", "true", "http://sport.bt.com/btsportplayer/bt-sport-2-01363810201819"]

    print "logging in"
    login = BtSportLogin(USERNAME, PASSWORD)
    cookies = login.get_cookies()
    for cookie in cookies:
        args.append(cookie[0])
        args.append(cookie[1])

    print args

    subprocess.call(args)
