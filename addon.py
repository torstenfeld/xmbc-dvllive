# -*- coding: utf-8 -*-

import re
import random
import string
from xbmcswift2 import Plugin, xbmc, xbmcaddon
from dvllive.web import Dvllive
from mymixpanel import Mixpanel
from pyxbmct.addonwindow import *

is_mixpanel_available = 'no'

class WindowVideoDetails(AddonDialogWindow):
    def __init__(self, title='test', url=None):
        # You need to call base class' constructor.
        super(WindowVideoDetails, self).__init__(title)
        # Set the window width, height and the grid resolution: 2 rows, 3 columns.
        # self.setGeometry(350, 150, 2, 3)
        self.setGeometry(850, 550, 2, 3)
        # Create a text label.
        label = Label('Video Details', alignment=ALIGN_CENTER)
        # Place the label on the window grid.
        self.placeControl(label, 0, 0, columnspan=3)
        # Create a button.
        button = Button('Close')
        # Place the button on the window grid.
        self.placeControl(button, 1, 1)
        # Set initial focus on the button.
        self.setFocus(button)
        # Connect the button to a function.
        listitem = xbmcgui.ListItem('Ironman')
        listitem.setInfo('video', {'Title': 'Ironman', 'Genre': 'Science Fiction'})
        self.connect(button, lambda: self._play_video(url, listitem))
        # Connect a key action to a function.
        self.connect(ACTION_NAV_BACK, self.close)

    def _play_video(self, url, listitem=None):
        mp.track('action', properties={
            'action': 'play_video',
            'videolink': url
        })
        player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
        player.play(url, listitem)
        self.close()

# Create a class for our UI
class MyAddon(AddonDialogWindow):
    def __init__(self, title=''):
        """Class constructor"""
        # Call the base class' constructor.
        super(MyAddon, self).__init__(title)
        # Set width, height and the grid parameters
        self.setGeometry(300, 230, 4, 2)
        # Call set controls method
        self.set_controls()
        # Call set navigation method.
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(ACTION_NAV_BACK, self.close)

    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = Image('xbmc-logo.png')
        self.placeControl(image, 0, 0, rowspan=2, columnspan=2)
        # Text label
        label = Label('Your name:')
        self.placeControl(label, 2, 0)
        # Text edit control
        self.name_field = Edit('')
        self.placeControl(self.name_field, 2, 1)
        # Close button
        self.close_button = Button('Close')
        self.placeControl(self.close_button, 3, 0)
        # Connect close button
        self.connect(self.close_button, self.close)
        # Hello button.
        self.hello_buton = Button('Hello')
        self.placeControl(self.hello_buton, 3, 1)
        # Connect Hello button.
        self.connect(self.hello_buton, lambda:
        xbmc.executebuiltin('Notification(Hello %s!, Welcome to PyXBMCt.)' %
                            self.name_field.getText()))

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.name_field.controlUp(self.hello_buton)
        self.name_field.controlDown(self.hello_buton)
        self.close_button.controlLeft(self.hello_buton)
        self.close_button.controlRight(self.hello_buton)


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
            'path': plugin.url_for('show_info', stub=video['link'])
        }
        items.append(item)
    return items

@plugin.route('/showvideo/<stub>/')
def show_info(stub):
    mp.track('route', properties={
        'route': 'show_video',
        'stub': stub
    })
    # name = urllib.unquote(safename)
    url = dvllive.play_video(stub)
    # print asset
    # plugin.log.info('Playing url: %s' % 'asdf')
    # plugin.log.info('Playing url: %s' % asset)
    items = [{
        # 'label': name,
        'label': 'Start video',
        'path': plugin.url_for('play_video', url=url),
        # 'path': plugin.url_for('play_video', asset=asset),
        'is_playable': False,
        # 'is_playable': True,
    }]
    return items
    # return plugin.finish(items)

@plugin.route('/showrtmp/<url>/')
def show_rtmp(url):
    mp.track('action', properties={
        'action': 'show_rtmp',
        'streamurl': url
    })
    item = {
        'label': 'rtmp',
        'path': 'rtmp://fms.12E5.edgecastcdn.net/0012E5/mp4:videos/8Juv1MVa-485.mp4'
    }
    return plugin.play_video(item)

@plugin.route('/playvideo/<url>')
def play_video(url):
    # Create a window instance.
    window = WindowVideoDetails('Hello, World!', url=url)
    # Show the created window.
    window.doModal()


if __name__ == '__main__':
    plugin.run()

# mydisplay = MyDisplay()
# mydisplay.doModal()
# del mydisplay

