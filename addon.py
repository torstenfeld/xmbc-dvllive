# -*- coding: utf-8 -*-

# import urllib
# import urllib2
# import re
# import sys
# import xbmc
# import xbmcplugin
# import xbmcaddon
# import xbmcgui
from xbmcswift2 import Plugin, xbmcaddon
from dvllive.web import Dvllive
# from pyxbmct.addonwindow import *


addon = xbmcaddon.Addon('plugin.video.dvllive')

plugin = Plugin()
dvllive = Dvllive()

@plugin.route('/')
def index():
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
    item = {
        'label': 'rtmp',
        'path': 'rtmp://fms.12E5.edgecastcdn.net/0012E5/mp4:videos/8Juv1MVa-485.mp4'
    }
    return plugin.play_video(item)


# class MyDisplay(AddonFullWindow):
#     hello_button = None
#     close_button = None
#     name_field = None
#     title_list = None
#     videos = []
#
#     def __init__(self, title=''):
#         # Call the base class' constructor.
#         super(MyDisplay, self).__init__(title)
#
#         self._dvllive = Dvllive()
#         self.videos_refresh()
#
#         # Set width, height, row, columns
#         self.setGeometry(900, 630, 10, 5)
#         # Call set controls method
#         self.set_controls()
#         # Call set navigation method.
#         self.set_navigation()
#         # Connect Backspace button to close our addon.
#         self.connect(ACTION_NAV_BACK, self.close)
#
#     def videos_refresh(self):
#         self._dvllive.get_videos()
#         self.videos = self._dvllive.videos_found
#
#     def set_controls(self):
#          """Set up UI controls"""
#          # Image control
#          image = Image('xbmc-logo.png')
#          self.placeControl(image, 0, 0, rowspan=2, columnspan=5)
#          # List
#          self.title_list = List()
#          self.placeControl(self.title_list, 2, 0, rowspan=7, columnspan=5)
#          # for i in range(1, 4):
#          for video in self.videos:
#             self.title_list.addItem(video['title'])
#          # Text label
#          # label = Label('Your name:')
#          # self.placeControl(label, 3, 0)
#          # Text edit control
#          # self.name_field = Edit('')
#          # self.placeControl(self.name_field, 3, 1)
#          # Close button
#          self.close_button = Button('Close')
#          self.placeControl(self.close_button, 9, 0)
#          # Connect close button
#          self.connect(self.close_button, self.close)
#          # Hello button.
#          self.hello_button = Button('Hello')
#          self.placeControl(self.hello_button, 9, 1)
#          # Connect Hello button.
#          # self.connect(self.hello_button, lambda: xbmc.executebuiltin('Notification(Hello %s!, Welcome to PyXBMCt.)' % self.videos[1]['title']))
#          # xbmc.executebuiltin('Notification(Hello %s!, Welcome to PyXBMCt.)' % self.name_field.getText()))
#
#     def set_navigation(self):
#          """Set up keyboard/remote navigation between controls."""
#          self.title_list.controlLeft(self.hello_button)
#          # self.name_field.controlUp(self.hello_button)
#          # self.name_field.controlDown(self.hello_button)
#          self.close_button.controlLeft(self.hello_button)
#          self.close_button.controlRight(self.hello_button)
#          self.close_button.controlUp(self.title_list)
#          self.close_button.controlDown(self.title_list)
#          self.hello_button.controlLeft(self.close_button)
#          self.hello_button.controlRight(self.close_button)
#          self.hello_button.controlUp(self.title_list)
#          self.hello_button.controlDown(self.title_list)
#          # self.hello_button.setNavigation(self.name_field, self.name_field, self.close_button, self.close_button)
#          # Set initial focus.
#          self.setFocus(self.title_list)


if __name__ == '__main__':
    plugin.run()

# mydisplay = MyDisplay()
# mydisplay.doModal()
# del mydisplay

