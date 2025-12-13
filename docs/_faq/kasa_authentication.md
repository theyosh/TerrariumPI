---
title: Kasa authentication error
categories: [Website, FAQ]
tags: [logging]
---

When you see the following error in the TerrariumPI logging you need to enable
`Third-Party Compatibility feature` in the app.

```
2025-12-11 03:47:55,212 - ERROR   - hardware.relay.kasa_relay - Server response doesn't match our challenge on ip 192.168.1.XXX
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
kasa.exceptions.AuthenticationException: Server response doesn't match our challenge on ip 192.168.1.XXX
```

More information can be found at the [Kasa relay
page]({% link _hardware/tplinkkasa_relay.md %})
