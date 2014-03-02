# -*- coding: utf-8 -*-

# import urllib
# import urllib2
# import re
# import sys
# import xbmc
# import xbmcplugin
# import xbmcaddon
# import xbmcgui
from dvllive.web import Dvllive
from pyxbmct.addonwindow import *


addon = xbmcaddon.Addon('plugin.video.dvllive')
__author__ = 'Torsten'

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
# ACTION_PREVIOUS_MENU = 10
# ACTION_SELECT_ITEM = 7
# ACTION_PARENT_DIR = 9


class MyDisplay(AddonDialogWindow):
    def __init__(self, title=''):
        self._dvllive = Dvllive()
        self._dvllive.get_videos()
        self.videos = self._dvllive.videos_found
        # Call the base class' constructor.
        super(MyDisplay, self).__init__(title)
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
         xbmc.executebuiltin('Notification(Hello %s!, Welcome to PyXBMCt.)' % self.videos[0]['title']))
         # xbmc.executebuiltin('Notification(Hello %s!, Welcome to PyXBMCt.)' % self.name_field.getText()))

    def set_navigation(self):
         """Set up keyboard/remote navigation between controls."""
         self.name_field.controlUp(self.hello_buton)
         self.name_field.controlDown(self.hello_buton)
         self.close_button.controlLeft(self.hello_buton)
         self.close_button.controlRight(self.hello_buton)
         self.hello_buton.setNavigation(self.name_field, self.name_field, self.close_button, self.close_button)
         # Set initial focus.
         self.setFocus(self.name_field)


mydisplay = MyDisplay()
mydisplay.doModal()
del mydisplay

