---
title: Reset authentication
categories: [Website, FAQ]
tags: [authentication]
---
When you loose your password, there is no way to retrieve it. So you need to manually reset it. Use the following steps to clear your existing password, and generate a new one.

1. Stop TerrariumPI ([FAQ]({% link _faq/systemd.md %}#stop))
2. Enter the TerrariumPI folder `cd /home/pi/TerrariumPI/data`
3. Load the database `sqlite3 terrariumpi.db`
4. Delete admin password `delete from Setting where id = 'password';`
5. Exit sqlite3 by pressing `Ctrl+D`
6. Start TerrariumPI ([FAQ]({% link _faq/systemd.md %}#start))

Now you should be able to login with chosen [username]({% link _tabs/setup.md %}#system) and password **password**
