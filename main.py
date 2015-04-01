#!/usr/bin/env python
# -*-coding: utf8 -*-

import wx
import webbrowser
from httpserver import HttpServer

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon/network.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, port_number):
        super(TaskBarIcon, self).__init__()
        self.port_number = port_number
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_double_click)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open', self.on_double_click)
        create_menu_item(menu, 'Settings', self.on_settings)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_double_click(self, event):
        webbrowser.open('http://localhost:%d' % (self.port_number,), new=0, autoraise=True)

    def on_settings(self, event):
        print 'Settings window.'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)


def main():
    a = HttpServer()
    port_number = 1112
    a.run(port_number)

    app = wx.App(False)
    TaskBarIcon(port_number)
    app.MainLoop()


if __name__ == '__main__':
    main()