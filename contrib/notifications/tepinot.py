# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#kahuwi14
#TerrariumPiNotification
#Version: 0.1
#Dependencies: ntfy, pygtail, parse
#https://pypi.python.org/pypi/ntfy
#https://pypi.python.org/pypi/pygtail
#https://pypi.python.org/pypi/parse


import ntfy
import datetime
import os
import pygtail
from ntfy.config import load_config
from pygtail import Pygtail
from datetime import date
from parse import *

conffile_str = '/home/pi/TerrariumPI/contrib/notifications/tepinot.conf'

lvlsearch_list = []
modulesearch_list = []
tplog_str = ''
ntfyconfig_str = ''
logfile_str = ''
sentmsg_int = 0
debug_bool = True

try:
    conffile_obj = open(conffile_str,"r") #open TePiNot-config

except OSError:
    print("%s - Can't open %s" %(datetime.datetime.now(), conffile_str.strip()))

except:
    print(datetime.datetime.now(), " - Unexpected error: ", sys.exc_info())

else:
    for line in conffile_obj: #read config-file
        if 'terrariumpi-log' in line.lower():
            switch = 1
        elif 'modules' in line.lower():
            switch = 2
        elif 'level' in line.lower():
            switch = 3
        elif 'ntfy-config' in line.lower():
            switch = 4
        elif 'debug-mode' in line.lower():
            switch = 5
        elif 'tepinot-log' in line.lower():
            switch = 6
        elif line.find('#') == -1 and line.strip():
            if switch == 1:
                tplog_str = format(line.strip())
            elif switch == 2:    
                modulesearch_list.append(format(line.strip()))
            elif switch == 3:
                lvlsearch_list.append(format(line.strip()))
            elif switch == 4:
                ntfyconfig_str = format(line.strip())
            elif switch == 5:
                if "on" in line.lower():
                    debug_bool = False
            elif switch == 6:
                logfile_str = format(line.strip())
    conffile_obj.close() #close TePiNot-config
    try:
        props = os.stat(logfile_str.strip())
        if not datetime.date.today() == datetime.date.fromtimestamp(props[8]):
            os.renames(logfile_str.strip(), logfile_str.strip() + '_' + str(datetime.date.fromtimestamp(props[8])))
        logfile_obj = open(logfile_str,"a") #open TePiNot-log

    except OSError:
        print("%s - Can't open %s" %(datetime.datetime.now(), logfile_str.strip()))

    else:
        if debug_bool: logfile_obj.write('%s - reading TerrariumPI-Log: %s\n' %(datetime.datetime.now(), tplog_str))
        for line_str in Pygtail(tplog_str):
            if debug_bool: logfile_obj.write('%s - parsing Line-String: %s\n' %(datetime.datetime.now(), line_str.strip()))
            for lvlsearch_str in lvlsearch_list:
                if debug_bool: logfile_obj.write('%s - searching Lvl-String: %s\n' %(datetime.datetime.now(), lvlsearch_str))
                for modulesearch_str in modulesearch_list:
                    if debug_bool: logfile_obj.write('%s - searching Module-String: %s\n' %(datetime.datetime.now(), modulesearch_str))
                    if lvlsearch_str in line_str and modulesearch_str in line_str:
                           if not "999" in line_str: #This is to prevent getting a message, everytime a sensor reports a false value
                                timestamp_acst, lvl_str, module_str, message_str = parse('{} - {} - {} - {}', line_str)
                                if not debug_bool:
                                    if not ntfyconfig_str:
                                        ntfy.notify(message_str, module_str.strip()+'-'+lvl_str.strip())                      
                                    else:
                                        ntfy.notify(message_str, module_str.strip()+'-'+lvl_str.strip(), config=load_config(ntfyconfig_str.strip()))
                                else:
                                    logfile_obj.write('%s - Notify-Message: %s\n\n' %(datetime.datetime.now(), message_str))    
                                sentmsg_int+=1
    
        logfile_obj.write('%s - %s read and %d messages sent.\n' %(datetime.datetime.now(), tplog_str.strip(), sentmsg_int))
        logfile_obj.close() #close TePiNot-log
