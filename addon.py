import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from BeautifulSoup import BeautifulSoup
import re

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
my_addon = xbmcaddon.Addon()


xbmcplugin.setContent(addon_handle, 'movies')

headers = {'Referer': 'https://longnow.org/membership/signin/'}
lp = requests.get('https://longnow.org/membership/signin/?next=/seminars/list', headers=headers)

if lp.status_code!=200:
    xbmcgui.Dialog().ok("Can't access login page.","HTTP status code is "+listpage.status_code)

loginSoup=BeautifulSoup(lp.text)
form= loginSoup.find("form")
token=loginSoup.find("input", {"name":"csrfmiddlewaretoken"})

username=my_addon.getSetting('username')
password=my_addon.getSetting('password')

if (username is None) or (username==""):
    xbmcgui.Dialog().ok("Invalid Username","Please enter a username in the settings of this plugin")
if (password is None) or (password==""):
    xbmcgui.Dialog().ok("Invalid Password","Please enter a password in the settings of this plugin")

data= {
    'username': username,
    'password': password,
    'next': '/seminars/list',
    'csrfmiddlewaretoken': token['value']
    }

r = requests.post('https://longnow.org/membership/signin/', data=data, headers=headers,cookies=lp.cookies)

listpage=r

if listpage.status_code!=200:
    xbmcgui.Dialog().ok("Can't access seminar list page.","HTTP status code is "+listpage.status_code,"Are username and password correct?")

listSoup=BeautifulSoup(listpage.text)
hdstring=re.compile('Full HD Video');
for dl in listSoup.findAll("ul", 'download_list'):
    hdlink=dl.find('a',title=hdstring);
    if hdlink is not None:
      name=dl.parent.parent.find('td',{'class':'title'}).a.string
      url=hdlink['href'];

      li = xbmcgui.ListItem(name, iconImage='DefaultVideo.png')
      xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
xbmcplugin.endOfDirectory(addon_handle)
