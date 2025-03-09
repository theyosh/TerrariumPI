---
title: Known errors
categories: [Website, FAQ]
tags: [errors]
---

The software can produce some warning and deprecation messages. And here is a
list of known messages which you can ignore.

## Bottle

```text
/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/bottle.py:3383: DeprecationWarning: Absolute template path names are deprecated.
  fname = self.search(name, self.lookup)
```

This message is very old, and TerrariumPI does not use bottle template engines.
So this message can be ignored.

## Cryptography

```text
/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/telegram/_passport/credentials.py:25: CryptographyDeprecationWarning: Python 3.7 is no longer supported by the Python core team and support for it is deprecated in cryptography. A future release of cryptography will remove support for Python 3.7.
  from cryptography.hazmat.backends import default_backend
```

This is a warning that in the next update of Cryptography, python 3.7 is not
supported anymore. This impacts only old buster OS. For now, we can still use
it.
