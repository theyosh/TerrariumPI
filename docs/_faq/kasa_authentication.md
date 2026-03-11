---
title: Kasa/Tapo authentication error
categories: [Website, FAQ]
tags: [authentication, error, kasa, tapo]
---

When you see the following error in the TerrariumPI logging you need to enable
`Third-Party Compatibility feature` in the app.

## Kasa error

```python
2025-12-11 03:47:55,212 - ERROR   - hardware.relay.kasa_relay - Server response does not match our challenge on ip 192.168.1.XXX
Traceback (most recent call last):
  File "/TerrariumPI/hardware/relay/kasa_relay.py", line 75, in _get_hardware_value
    data = self.__asyncio.run(__get_hardware_state())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/TerrariumPI/terrariumUtils.py", line 65, in run
    return data.result()
           ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/concurrent/futures/_base.py", line 456, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/TerrariumPI/hardware/relay/kasa_relay.py", line 63, in __get_hardware_state
    await self.device.update()
  File "/opt/venv/lib/python3.11/site-packages/kasa/smartdevice.py", line 353, in update
    response = await self.protocol.query(req)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/kasa/iotprotocol.py", line 43, in query
    return await self._query(request, retry_count)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/kasa/iotprotocol.py", line 59, in _query
    raise auex
  File "/opt/venv/lib/python3.11/site-packages/kasa/iotprotocol.py", line 48, in _query
    return await self._execute_query(request, retry)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/kasa/iotprotocol.py", line 86, in _execute_query
    return await self._transport.send(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/kasa/klaptransport.py", line 309, in send
    await self.perform_handshake()
  File "/opt/venv/lib/python3.11/site-packages/kasa/klaptransport.py", line 279, in perform_handshake
    local_seed, remote_seed, auth_hash = await self.perform_handshake1()
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/kasa/klaptransport.py", line 233, in perform_handshake1
    raise AuthenticationException(msg)
kasa.exceptions.AuthenticationException: Server response does not match our challenge on ip 192.168.1.XXX
```

More information can be found at the [Kasa relay
page]({% link _hardware/tplinkkasa_relay.md %})

## Tapo

```python
2026-03-11 11:54:02,902 - WARNING - terrariumRelay        - Could not load hardware for relay TAPO P100/5 relay named 'Heat mat' at address '...': Failed to initialize protocol, retrying in 0.5 seconds...
Exception: Error code: 1003
    raise Exception(f"Error code: {data['error_code']}")
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/auth_protocol.py", line 173, in _request_raw
    result = self._request_raw("handshake", {"key": public_key})
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/auth_protocol.py", line 244, in Initialize
    protocol.Initialize()
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/PyP100.py", line 35, in _initialize
Traceback (most recent call last):
2026-03-11 11:54:02,890 - ERROR   - PyP100.PyP100         - Failed to initialize protocol OldProtocol
2026-03-11 11:54:02,882 - ERROR   - root                  - Wrong message formatting invalid syntax (<string>, line 1)
2026-03-11 11:54:02,877 - ERROR   - PyP100.auth_protocol  - Error: {'error_code': 1003}
requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: http://the.ip/app/handshake1
    raise HTTPError(http_error_msg, response=self)
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/requests/models.py", line 1026, in raise_for_status
    resp.raise_for_status()
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/auth_protocol.py", line 45, in _request_raw
    response = self._request_raw("handshake1", local_seed)
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/auth_protocol.py", line 95, in Initialize
    protocol.Initialize()
  File "/home/pi/TerrariumPI/venv/lib/python3.9/site-packages/PyP100/PyP100.py", line 35, in _initialize
```

More information can be found at the [Tapo P100 relay
page]({% link _hardware/tapo_p100_relay.md %})
