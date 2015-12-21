# -*- coding: utf-8 -*-
import grp
import pwd
import os
import sys
from subprocess import call

username = 'dalexandrov'
wwwdir = '/home/' + username + '/www/'

# Colours to decorate output
class bgcolors:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	ENDC = '\033[0m'

# Check root access
def check_root():
    uid = os.getuid()
    if uid != 0:
            sys.exit('Not superuser')

# Ask for a sitename and return value
def ask_sitename():
    print ('What\'s your site name?')
    sitename = raw_input().lower()
    return sitename

# Creating directory based on a given sitename and placing basic index.php file in it
def create_site_dir():
    print bgcolors.BLUE + 'Creating a directory ' + sitename + '.dev under ' + wwwdir + bgcolors.ENDC
    os.makedirs(wwwdir + sitename + '.dev')
    inx = open(wwwdir + sitename + '.dev/index.php', 'w')
    inx.write('Hello')
    inx.close()
    print bgcolors.GREEN + 'Done' + bgcolors.ENDC

# Give specified user access to a newely created folder and its conents
def set_user_rights():
    print bgcolors.BLUE + 'Giving ' + username + ' permissions for ' + wwwdir + sitename + '.dev' + bgcolors.ENDC
    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(username).gr_gid
    os.chown(wwwdir + sitename + '.dev', uid, gid)
    os.chown(wwwdir + sitename + '.dev/index.php', uid, gid)
    print bgcolors.GREEN + 'Done' + bgcolors.ENDC

# Create and write apache config file
def create_site_config():
    text = [
    '<VirtualHost *:80>',
    'ServerName ' + sitename + '.dev',
    'ServerAlias www.' + sitename + '.dev',
    'DocumentRoot ' + wwwdir + sitename + '.dev',
    'SetEnv APPLICATION_ENV "dev"',
    '<Directory ' + wwwdir + sitename + '.dev/>',
    'AllowOverride All',
    'Require all granted',
    '</Directory>',
    '</VirtualHost>']

    print bgcolors.BLUE + 'Writing apache conf file' + bgcolors.ENDC
    conf = open("/etc/apache2/sites-available/" + sitename + ".dev.conf", 'w')

    for index in text:
            conf.write(index + '\n')

    conf.close()
    print bgcolors.GREEN + 'Done' + bgcolors.ENDC

# Update hosts
def update_hosts():
    print bgcolors.BLUE + 'Updating hosts file' + bgcolors.ENDC
    hosts = open("/etc/hosts", 'a')
    hosts.write('\n\n' + sitename.capitalize() + '\n')
    hosts.write("127.0.0.1 " + sitename + ".dev www." + sitename + ".dev" + '\n')
    hosts.close()
    print bgcolors.GREEN + 'Done' + bgcolors.ENDC

# Enable new virtual host and restart apache
def turn_on():
    print "Enabling " + sitename + ".dev and restarting service"

    with open(os.devnull, "w") as f:
        call(["a2ensite", sitename + '.dev'], stdout=f)

    call(["service", "apache2", "restart"])

check_root()
sitename = ask_sitename()
create_site_dir()
set_user_rights()
create_site_config()
update_hosts()
turn_on()

print bgcolors.GREEN + 'All done' + bgcolors.ENDC