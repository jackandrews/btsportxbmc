import cookielib
import urllib
import urllib2
import re
import random


class BtSportLogin:

    def __init__(self, user, password):
        self.cj = cookielib.CookieJar()
        url = 'https://signin1.bt.com/siteminderagent/forms/login.fcc'
        #authURL = self.GetAuthURL()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
        post_data = {'cookieExpp': 30,
                     'Switch': 'yes',
                     'SMPostLoginUrl': '/appsyouraccount/secure/postlogin',
                     'loginforward': 'https://sport.bt.com/ss/Satellite/secure/loginforward',
                     'smauthreason': 0,
                     'TARGET': 'https://sport.bt.com/ss/Satellite/secure/loginforward?redirectURL=http%3A%2F%2Fsport%2Ebt%2Ecom%2F',
                     'USER': user,
                     'PASSWORD': password}
        post = urllib.urlencode(post_data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        request = urllib2.Request(url, post, headers)
        response = opener.open(request)
        resp = response.read()

    def get_cookies(self):
        cookies = []
        for cookie in self.cj:
            cookies.append([cookie.name, cookie.value])
        return cookies
