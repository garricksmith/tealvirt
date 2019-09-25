#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# TEALVirt VMWindow UI
#
# Author:   Garrick Smith <gdsmith1@coastal.edu>
# Revision: 19 August 2019
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class VMWindow(Gtk.Window):
    
    def __init__(self, ve):
        Gtk.Window.__init__(self, title='TealVIRT Virtual Machine Manager')
        self.ve = ve
        self.selected_vm = None
        self.vm_status_label = None
        
        # Define container that will hold all of the contents for the page
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(container)
        
        # Define toolbar container that contains a back, start, stop,
        # screenshot, log, and trash buttons mapped to the ve and its methods 
        # that correspond to the button label
        labels = ['Start', 'Stop', 'Screenshot', 'Trash']
        toolbar = Gtk.Toolbar.new()
        for label in labels:
            button = Gtk.ToolButton.new()
            button.set_label(label)
            button.connect('clicked', self.on_main_toolbar_clicked)
            toolbar.insert(button, -1)
        #
        container.pack_start(toolbar, False, False, 0)
        
        separator = Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL)
        container.pack_start(separator, False, False, 0)
        
        # Define hbox container that will hold the list of vms and the status
        # window associated with the selected vm
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        container.pack_start(hbox, True, True, 0)
        
        # Define scroller container that is used for the list of vms and add the
        # vmlist container to the scroller container
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        
        vmlist = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        scroller.add(vmlist)
        hbox.pack_start(scroller, True, True, 0)
        
        label = Gtk.Label()
        label.set_text('VM List')
        vmlist.pack_start(label, False, True, 10)
        
        self.selected=''
        for vm in ve.vms:
            button = Gtk.ToggleButton()
            button.set_label(vm.name)
            button.set_name(str(vm.vmid))
            button.connect('clicked', self.on_button_toggled)
            vmlist.pack_start(button, False, True, 0)
        #
        
        # Define vmstatus container that will hold all of the contents and
        # controls of the selected vm
        self.vmstatus = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label()
        label.set_text('Please Select a VM to Display its Status')
        
        self.vmstatus.pack_start(label, True, True, 0)
        hbox.pack_start(self.vmstatus, True, True, 0)
        
        # Set the border size of the window to fit the containers properly and 
        # add thicker border
        self.set_border_width(10)
        self.set_size_request(650,500)
    #
    
    def on_button_toggled(self, button):
        if button.get_active():
            if not self.selected:
                self.selected = button
                for vm in self.ve.vms:
                    vmid = str(vm.vmid)
                    if vmid == self.selected.get_name():
                        self.selected_vm = vm
                    #
                #
                self.set_vm_status()
            else:
                self.selected.set_active(False)
                self.selected = button
                for vm in self.ve.vms:
                    vmid = str(vm.vmid)
                    if vmid == self.selected.get_name():
                        self.selected_vm = vm
                    #
                #
                self.set_vm_status()
            #
        else:
            self.selected = None
        #
    #
    
    def on_main_toolbar_clicked(self, button):
        button_label = button.get_label()
        if button_label == 'Start':
            self.ve.start()
        elif button_label == 'Stop':
            self.ve.stop()
        elif button_label == 'Screenshot':
            self.ve.screenshot()
        elif button_label == 'Trash':
            self.ve.trash()
        #
    #
    
    def on_vm_toolbar_clicked(self, button):
        button_label = button.get_label()
        if button_label == 'Start':
            self.selected_vm.start()
            self.vm_status_label.set_text('Status: ' + self.selected_vm.status())
            self.vm_status_label.show_all()
        elif button_label == 'Stop':
            self.selected_vm.stop()
            self.vm_status_label.set_text('Status: ' + self.selected_vm.status())
            self.vm_status_label.show_all()
        elif button_label == 'Rollbacks':
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            label = Gtk.Label()
            label.set_text('Rollbacks:')
            vbox.pack_start(label, False, True, 5)
            
            for disk in self.selected_vm.command.disks:
                if disk.overlay == True:
                    rollback_disk = disk #Selected first disk with overlay
                    pass
                #
            #
            snapshots = rollback_disk.get_snapshots()
            for snapshot in snapshots:
                button = Gtk.Button()
                button.connect('clicked', self.on_snapshot_clicked)
                button.set_label(snapshot)
                vbox.pack_start(button, False, True, 0)
            #
            self.vmstatus.pack_start(vbox)
        elif button_label == 'Console':
            # Not sure what to do here...
            pass
        #
    #
    
    def on_snapshot_clicked(self, button):
        snapshot = button.get_label()
        if self.selected_vm.status() == 'Running':
            print('ERROR: Cannot rollback while vm is running')
        else:
            for disk in self.selected_vm.command.disks:
                if disk.overlay == True:
                    rollback_disk = disk #Selected first disk with overlay
                    pass
                #
            #
            rollback_disk.rollback(snapshot)
        #
    #
    
    def set_vm_status(self):
        # Clear Contents of VMStatus Container
        children = self.vmstatus.get_children()
        for child in children:
            self.vmstatus.remove(child)
        #
        
        # Define VMStatus Label in a Container
        hbox = Gtk.Box()
        
        label = Gtk.Label()
        label.set_text('Selected VM: ' + self.selected.get_label())
        hbox.pack_start(label, True, True, 0)
        
        self.vm_status_label = Gtk.Label()
        self.vm_status_label.set_text('Status: ' + self.selected_vm.status())
        hbox.pack_start(self.vm_status_label, True, True, 0)
        
        separator = Gtk.Separator.new(orientation=Gtk.Orientation.VERTICAL)
        
        self.vmstatus.pack_start(hbox, False, True, 0)
        self.vmstatus.pack_start(separator, False, True, 5)
        
        # Define VMStatus Toolbar
        labels = ['Start', 'Stop', 'Rollbacks', 'Console']
        toolbar = Gtk.Toolbar.new()
        for label in labels:
            button = Gtk.ToolButton.new()
            button.connect('clicked', self.on_vm_toolbar_clicked)
            button.set_label(label)
            toolbar.insert(button, -1)
        #
        self.vmstatus.pack_start(toolbar, False, True, 0)
        
        # Display new vmstatus container
        self.vmstatus.show_all()
    #
#

def display_vmwindow(ve):
    win = MainWindow(ve)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
#

'''
 BELOW USED FOR TESTING ONLY
'''

if __name__ == '__main__':
    class VE:
        def __init__(self):
            self.status = None
            self.vms = (VM('VM 0',0),VM('VM 1',1),VM('VM 2',2),VM('VM 3',3))
        #
        
        def start(self):
            self.status = 'Running'
            print('VE Started')
        #
        
        def stop(self):
            self.status = 'Stopped'
            print('VE Stopped')
        #
        
        def status(self):
            return self.status
        #
        
        def screenshot(self):
            print('Screenshot of VE taken')
        #
        
        def get_vm(self,vmid):
            for vm in vms:
                if vmid == vm.vmid:
                    return vm
                #
            #
        #
        
        def trash(self):
            print('VE has been trashed')
        #
    #
    
    class VM:
        def __init__(self, name, vmid):
            self.vmstatus = 'Stopped'
            self.name = name
            self.vmid = vmid
        #
        
        def start(self):
            if self.vmstatus == 'Stopped':
                self.vmstatus = 'Running'
                print('VM Started')
            else:
                print('VM is already running')
                return
            #
        #
        
        def stop(self):
            if self.vmstatus == 'Running':
                self.vmstatus = 'Stopped'
                print('VM Stopped')
            else:
                print('VM is already stopped')
                return
            #
        #
        
        def status(self):
            return self.vmstatus
        #
    #
    
    ve = VE()
    win = VMWindow(ve)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
#
