---
title: Reset authentication
categories: [Website, FAQ]
tags: [authentication]
permalink: /faq/:title/
---
When you loose your password, there is no way to retreive it. So you need to manually reset it. Use the following steps to clear your existing password, and generate a new one.

1. Stop TerrariumPI ([FAQ]({{ 'faq/systemd/' | relative_url}}#stop))
2. Enter the TerrariumPI folder `cd /home/pi/TerrariumPI`
3. Load the database `sqlite3 terrariumpi.db`
4. Delete admin password `delete from Setting where id = 'password';`
5. Exit sqlite3 by pressing `Ctrl+D`
6. Start TerrariumPI ([FAQ]({{ 'faq/systemd/' | relative_url}}#start))

Now you should be able to login with chosen [username]({{ 'setup/' | relative_url}}#system) and password **password**