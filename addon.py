# -*- coding: utf-8 -*-

import re
import random
import string
from xbmcswift2 import Plugin, xbmc, xbmcaddon
from dvllive.web import Dvllive
from mymixpanel import Mixpanel

is_mixpanel_available = 'no'

class MyMixpanel(object):
    _mptoken = 'fed95492dc111b7805684b04ec2d0ce6'
    # _mptoken = 'a0d1edc9e04bfea65ccce4ac9d99c62f'

    def __init__(self):
        self._mp = Mixpanel(self._mptoken)
        global is_mixpanel_available
        is_mixpanel_available = 'yes'
        self._id = self._get_uniqueid()
        self._ip = xbmc.getIPAddress()
        self._lang = xbmc.getLanguage()
        self._mp.people_set(self._id, {
            'ip': self._ip,
            'lang': self._lang
        })
        self.track('start')
        return None

    def _get_uniqueid(self):
        if 'isRandom' in cache:
            if not cache['isRandom']:
                # self._id already correct
                uid = cache['uid']
            else:
                # self._id not yet correct
                if self._check_mac():
                    cache['isRandom'] = False
                    uid = cache['uid']
                else:
                    cache['isRandom'] = True
                    cache['uid'] = self._create_randomid()
                    uid = cache['uid']
        else:
            # neither correct nor random id
            if self._check_mac():
                cache['isRandom'] = False
                uid = cache['uid']
            else:
                cache['isRandom'] = True
                cache['uid'] = self._create_randomid()
                uid = cache['uid']

        for i in range(0, 10):
            print 'mac: %s / uid: %s' % (cache['mac'], uid,)
        return uid

    @staticmethod
    def _check_mac():
        mac = xbmc.getInfoLabel('Network.MacAddress')
        cache['mac'] = mac
        if re.match('([a-hA-H0-9]{2}:){5}[a-hA-H0-9]{2}', mac):
            cache['uid'] = mac
            return True
        else:
            return False

    @staticmethod
    def _create_randomid():
        return ''.join(random.choice(string.letters) for i in range(40))


    def track(self, event_name, properties={}, meta={}):
        self._mp.track(self._id, event_name, properties, meta)
        return self

    def track_route(self, route_name):
        self.track('route', properties={
            'route': route_name
        })

addon_id = 'plugin.video.dvllive'
addon = xbmcaddon.Addon(addon_id)

plugin = Plugin()
cache = plugin.get_storage('cache')
mp = MyMixpanel()
dvllive = Dvllive()

@plugin.route('/')
def index():
    print 'is_mixpanel_available: ', is_mixpanel_available
    mp.track('route', properties={
        'route': 'index'
    })
    items = []
    dvllive.get_videos()
    for video in dvllive.videos_found:
        item = {
            'label': video['title'],
            'label2': 'test',
            'path': plugin.url_for('show_video', stub=video['link'])
        }
        items.append(item)
    return items

@plugin.route('/showvideo/<stub>/')
def show_video(stub):
    mp.track('route', properties={
        'route': 'show_video',
        'stub': stub
    })
    # name = urllib.unquote(safename)
    asset = dvllive.play_video(stub)
    # plugin.log.info('Playing url: %s' % 'asdf')
    plugin.log.info('Playing url: %s' % asset)
    items = [{
        # 'label': name,
        'label': 'name',
        'path': asset,
        'is_playable': True,
    }]
    return plugin.finish(items)

@plugin.route('/showrtmp/<url>/')
def show_rtmp(url):
    mp.track('route', properties={
        'route': 'show_rtmp',
        'stub': url
    })
    item = {
        'label': 'rtmp',
        'path': 'rtmp://fms.12E5.edgecastcdn.net/0012E5/mp4:videos/8Juv1MVa-485.mp4'
    }
    return plugin.play_video(item)


if __name__ == '__main__':
    plugin.run()

# mydisplay = MyDisplay()
# mydisplay.doModal()
# del mydisplay

