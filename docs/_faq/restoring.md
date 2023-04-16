---
title: Restoring backup files
categories: [Website, FAQ]
tags: [backup]
---
If you have made regular backups, than you can restore it with the following steps. If the backup has become corrupted, follow [these]({% link _faq/malformed_database.md %}) steps first.

- [Shutdown]({% link _faq/systemd.md %}#stop) TerrariumPI
- Remove the old files in `data` if there are any. `rm data/*`
- Place the backup files in the `data` folder.
- Place custom logging or webcam archives back in place if needed.
- [Start]({% link _faq/systemd.md %}#start) TerrariumPI

This should start TerrariumPI with the backup-ed data.
