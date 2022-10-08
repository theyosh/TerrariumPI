---
title: Tune database settings
categories: [Website, FAQ]
tags: [database,stability]
---
Currently the database SQLITE3 settings are setup for speed. And therefore it cannot handle power outages well. If you need for what ever reason a different SQLITE3 setup, you can create a file called `data/.database-env` with the following contents:

```
[pragma setting name]=[value]
```

All [SQLITE3 pragmas](https://www.sqlite.org/pragma.html) should be supported. Make sure you use the correct pragma name and value.

For example the current defaults are:

```console
auto_vacuum=NONE
cache_size=-10000
journal_mode=WAL
synchronous=OFF
temp_store=MEMORY
```

If you need more [stability](https://www.sqlite.org/howtocorrupt.html) you can use the following settings:

```console
synchronous=FULL
```