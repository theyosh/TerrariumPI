# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#kahuwi14
#Version: 0.3
#Dependencies: ntfy, pygtail
#https://pypi.python.org/pypi/ntfy
#https://pypi.python.org/pypi/pygtail


import ntfy
from ntfy.config import load_config
from pygtail import Pygtail
from datetime import date
from parse import *

conffile_str = "logcheck.conf"

lvlsearch_list=[]
modulesearch_list=[]
logfile_str=''
ntfyconfig_str=''

conffile_obj = open(conffile_str,"r")
for line in conffile_obj:
    if 'Logfile-path' in line:
        switch = 1
    elif 'Modules' in line:
        switch = 2
    elif 'Level' in line:
        switch = 3
    elif "ntfy-config" in line:
        switch = 4    
    elif line.find('#') == -1 and line.strip():
        if switch == 1:
            logfile_str = format(line.strip())
        elif switch == 2:    
            modulesearch_list.append(format(line.strip()))
        elif switch == 3:
            lvlsearch_list.append(format(line.strip()))
        elif switch == 4:
            ntfyconfig_str = format(line.strip())
conffile_obj.close()

for line_str in Pygtail(logfile_str):
    for lvlsearch_str in lvlsearch_list:
        for modulesearch_str in modulesearch_list:
            if lvlsearch_str in line_str and modulesearch_str in line_str:
                    if not "None" in line_str: #This is to prevent getting a message, everytime a sensor reports a false value
                        timestamp_acst, lvl_str, module_str, message_str = parse('{} - {} - {} - {}', line_str)
                        if not ntfyconfig_str:
                            ntfy.notify(message_str, module_str.strip()+'-'+lvl_str.strip())
                        else:
                            ntfy.notify(message_str, module_str.strip()+'-'+lvl_str.strip(), config=load_config(ntfyconfig_str.strip()))
