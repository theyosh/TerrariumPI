---
title: Reset webgui address
categories: [Website, FAQ]
tags: [database,gui,address,port,listening]
---
If you have configured a fixed IP as address and your PI has changed the IP due to a network change, the TerrariumPI software will not load the web gui. The system is still running, but you are unable to access the webgui.

An error could look like:

```console
2023-11-01 10:39:59,000 - INFO    - terrariumWebserver    - Running webserver at 192.168.1.2:8090
Traceback (most recent call last):
  File "terrariumPI.py", line 16, in <module>
    terrariumEngine = terrariumEngine(__version__)
  File "/home/pi/TerrariumPI/terrariumEngine.py", line 175, in __init__
    self.webserver.start()
  File "/home/pi/TerrariumPI/terrariumWebserver.py", line 306, in start
    quiet=True)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/bottle.py", line 767, in run
    run(self, **kwargs)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/bottle.py", line 3175, in run
    server.run(app)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/bottle_websocket/server.py", line 17, in run
    server.serve_forever()
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/baseserver.py", line 398, in serve_forever
    self.start()
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/baseserver.py", line 336, in start
    self.init_socket()
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/pywsgi.py", line 1545, in init_socket
    StreamServer.init_socket(self)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/server.py", line 180, in init_socket
    self.socket = self.get_listener(self.address, self.backlog, self.family)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/server.py", line 192, in get_listener
    return _tcp_listener(address, backlog=backlog, reuse_addr=cls.reuse_addr, family=family)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/server.py", line 288, in _tcp_listener
    sock.bind(address)
  File "/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/gevent/_socketcommon.py", line 563, in bind
    return self._sock.bind(address)
OSError: [Errno 99] Cannot assign requested address: ('192.168.1.2', 8090)
```

The solution for this is to reset the IP address that was entered. Here are the steps to fix it.

1. Stop TerrariumPI: `sudo service terrariumpi stop`
2. Enter the TerrariumPI folder: `cd /home/pi/TerrariumPI/`
3. Open the database with sqlite: `sqlite3 data/terrariumpi.db`
4. Run the following query statement: `DELETE FROM Setting WHERE id = 'host';`
5. Run the following query statement: `DELETE FROM Setting WHERE id = 'port';`
6. Exit the database by pressing `CTRL+d`
7. Start TerrariumPI: `sudo service terrariumpi start`

The steps 3 - 6 are shown below.

```console
sqlite3 data/terrariumpi.db
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
sqlite> DELETE FROM Setting WHERE id = 'host';
sqlite> DELETE FROM Setting WHERE id = 'port';
sqlite>
```

When TerrariumPI is started up, you should be able to access the web gui again on the new IP of the Raspberry PI
