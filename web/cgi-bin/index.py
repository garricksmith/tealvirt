#!/usr/bin/env python3
import cgi
import cgitb

from jinja2 import Environment, FileSystemLoader

##############################################################################
def display_ves(title, all_ves):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('ve-menu.html')

    output = template.render(
       title = title, all_ves = all_ves
    )

    print(output)
    return
#

def display_vms(title, vms):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('ve-status.html')

    output = template.render(
        title = title, vms = vms
    )

    print(output)
    return
#

def display_professors(title, professors):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('display-professors.html')
    
    output = template.render(
        title = title, professors = professors
    )
    
    print(output)
    return
#

def display_courses(title, courses):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('display-courses.html')
    
    output = template.render(
        title = title, courses = courses
    )
    
    print(output)
    return
#

def display_new_ves(title, ves):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('display-new-ves.html')
    
    output = template.render(
        title = title, ves = ves
    )
    
    print(output)
    return
#

def display_log(title, logs):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('ve-log.html')
    
    output = template.render(
        title = title, logs = logs
    )
    
    print(output)
    return
#

def display_rollbacks(title, rollbacks):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('ve-rollbacks.html')

    output = template.render(
        title = title, rollbacks = rollbacks
    )

    print(output)
    return
#

def init_page():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('base.html')

    output = template.render()

    print(output)
    return
#

def add_ve(ves, ve):
    ves.update({ve: 'Stopped'})
#

##############################################################################
cgitb.enable()
print('Content-Type: text/html')
print()

form = cgi.FieldStorage()
ves = {'CSCI-VIRT-00':'Running','CSCI-VIRT-01':'Stopped','CSCI-VIRT-02':'Stopped','CSCI-VIRT-03':'Stopped'}

if 'action' not in form and 'title' not in form:
    init_page()
else:
    action = form['action'].value
    title = form['title'].value
    
    if 've-name' not in form:
        if action == 'displayVEs':
            display_ves(title, ves)
        elif action == 'displayVMs':
            display_vms(title, ['VM-0', 'VM-1', 'VM-2', 'VM-3'])
        elif action == 'displayProfessors':
            display_professors(title, ['Mike Murphy', 'Cory Nance', 'Timothy Burke'])
        elif action == 'displayCourses':
            display_courses(title, ['CSCI-130', 'CSCI-225', 'CSCI-330', 'CSCI-490'])
        elif action == 'selectVE':
            display_new_ves(title, ['CSCI-VIRT-04', 'CSCI-VIRT-05'])
        elif action == 'displayLog':
            display_log(title, ['Log Item', 'Log Item', 'Log Item'])
        elif action == 'displayRollbacks':
            display_rollbacks(title, ['Rollback 1', 'Rollback 2', 'Rollback 3'])
        #
    else:
        ve = form['ve-name'].value
        
        if action == 'addVE':
            add_ve(ves, ve)
            display_ves(title, ves)
        #
    #
#
