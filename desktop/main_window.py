#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# TEALVirt Main Window UI
#
# Author:   Garrick Smith <gdsmith1@coastal.edu>
# Revision: 19 August 2019
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self, obj_list, list_attribute):
        self.obj_list = obj_list
        self.list_attribute = list_attribute
        
        Gtk.Window.__init__(self, title='TealVIRT Virtual Environment Menu')
        
        # Define container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(container)
        
        # Define scroll container
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        
        # Define button container within scroller container
        vbox = Gtk.Box(spacing=0)
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        scroller.add(vbox)
        
        # Add title label and scroller container
        label = Gtk.Label()
        label.set_text('Select Virtual Environment')
        container.pack_start(label, False, False, 10)
        container.pack_start(scroller, True, True, 0)
        
        # Add list of objects as toggle buttons
        for list_item in self.obj_list:            
            button = Gtk.ToggleButton()
            label = getattr(list_item, self.list_attribute)
            button.set_label(label)
            button.connect('toggled', self.on_button_toggled)
            vbox.pack_start(button, False, True, 0)
        #
        self.selected = None
        
        # Add submit button
        self.submit_button = Gtk.Button()
        self.submit_button.set_label('Submit')
        self.submit_button.connect('clicked', self.on_button_clicked)
        vbox.pack_start(self.submit_button, False, True, 15)
        
        self.set_border_width(10)
        self.set_size_request(450,300)
    #
    
    def on_button_toggled(self, button):
        if button.get_active():
            state = 'on'
            if not self.selected:
                self.selected = button
            else:
                self.selected.set_active(False)
                self.selected = button
            #
        else:
            state = 'off'
            self.selected = None
        #
    #
    
    def on_button_clicked(self, button):
        if self.selected:
            self.selected = self.selected.get_label()
            for i in self.obj_list:
                if getattr(i, self.list_attribute) == self.selected:
                    self.selected = i
                #
            #
            self.destroy()
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK, 'ERROR: MISSING INFORMATION')
            dialog.format_secondary_text('Please Make a Selection to Continue')
            dialog.run()
            print('ERROR dialog closed')
            dialog.destroy()
        #
    #
#

def display_main(select_list, list_attribute):
    win = MainWindow(select_list, list_attribute)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
    if win.selected:
        if isinstance(win.selected, type(select_list[0])):
            return win.selected
        else:
            return None
    else:
        return None
    #
#
'''
Below is code used for testing only, remove before putting into production
'''
class Professor:
    def __init__(self, name):
        self.name = name
    #
#

if __name__ == '__main__':
    professors = [Professor('John'), Professor('Steve'), Professor('Janice')]
    professor = display_main(professors, 'name')
    print(professor)
#
