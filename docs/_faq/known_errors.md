---
title: Known errors
categories: [Website, FAQ]
tags: [errors]
---

The software can produce some warning and deprecation messages. And here is a list of known messages which you can ignore.

## Bottle

```
/home/pi/TerrariumPI/venv/lib/python3.7/site-packages/bottle.py:3383: DeprecationWarning: Absolute template path names are deprecated.
  fname = self.search(name, self.lookup)
```

This message is very old, and TerrariumPI does not use bottle template engines. So this message can be ignored.
