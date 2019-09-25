#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# TEALVirt desktop application
#
# Author:   Dr. Mike Murphy <mmurphy2@coastal.edu>
#           Garrick Smith <gdsmith1@coastal.edu>
# Revision: 19 August 2019
#

import datetime
import logging
import sys
import threading
import time

from tealvirt.config.selector import VESelector
from tealvirt.config.userconfig import UserConfig
from tealvirt.config.veconfig import VEConfig
from tealvirt.desktop.main_window import display_main
from tealvirt.desktop.vm_window import display_vmwindow
from tealvirt.network.networkfactory import NetworkFactory
from tealvirt.ve.veobject import VirtualEnvironment

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DesktopApp:
    def __init__(self, user_config_file):
        self.network_factory = NetworkFactory()
        self.userconf = UserConfig(user_config_file)
        self.ve = None
    #
    def main(self):
        gtk_thread = threading.Thread(target=Gtk.main)

        # Garrick: you can move this code and merge it into the GUI code if
        # that makes more sense from a design perspective. These are the steps
        # that the code should take to get a VE going. DON'T CALL Gtk.main
        # from your code, since it's done in the above thread.

        selector = VESelector(self.userconf.get_source_root())
        professors = selector.get_professors()

        # User picks professor from list of professors provided, returns a 
        # professor object if selected and submitted, returns None if 
        # window is closed
        professor = display_main(professors, 'name')
        
        if not professor:
            sys.exit(1)
            
        courses = selector.get_courses(professor)
            
        # User picks course from list of course id's provided, returns a 
        # course object if selected and submitted, returns None if window is 
        # closed
        course = display_main(courses, 'id')
        
        if not course:
            sys.exit(1)
        #

        # User picks VE from list of VE friendly names provided, returns a
        # ve_list object if selected and submitted, returns None if window is
        # closed
        ve_config_path = display_main(course.ve_list, 'friendly_name')

        if not ve_config_path:
            sys.exit(1)
        #

        ve_config = VEConfig(self.userconf, ve_config_path)

        # GARRICK TODO: configure the logger here -- set it to write the
        # log to the log_target
        log_name = str(datetime.datetime.now())
        log_target = ve_config.get_log_path(log_name)
        GARRICK_POINT_LOG_TO(log_target)
        GARRICK_SET_LOG_LEVEL(idk)

        self.ve = VirtualEnvironment(ve_config, self.network_factory)

        # ve.start()
        # ve.stop()
        # ve.status()
        # ve.screenshot()
        # vm = ve.get_vm(vmid)
        #
        # The relevant VM-level methods are in qemu/process.py and are:
        #
        # vm.start()
        # vm.stop()
        # vm.status()   <-- probably don't need, since ve.status provides
        #
        # To get to the disk rollbacks:
        #
        # disks = vm.command.disks
        #
        # Pick a disk (only those where disk.overlay is True can do snapshots),
        # then:
        #
        # disk.get_snapshots (and present to the user, picking a single
        # snapshot object)
        # disk.rollback(snapshot) does the rollback
        #
        # CHECK that the VM is stopped before doing a disk rollback, or bad
        # shit will happen.
        win = display_vmwindow(self.ve)

        # Wait for Gtk to exit before quitting
        while gtk_thread.is_alive():
            time.sleep(2)
        #
    #
#

if __name__ == '__main__':
    import argparse
    import sys

    parser = \
        argparse.ArgumentParser(description='TEALVirt virtualization system')
    parser.add_argument('user_config_file', metavar='config_file', type=str, \
                        nargs=1, help='user.ini file')
    args = parser.parse_args()

    app = DesktopApp(args.user_config_file)
    app.main()
#




