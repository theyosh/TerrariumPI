#!/bin/bash

cd ..
mv views/inc/footer.tpl views/inc/footer.tpl_tmp
pygettext -v -a -n -o locales/terrariumpi.pot views/*.tpl views/inc/*.tpl *.py
mv views/inc/footer.tpl_tmp views/inc/footer.tpl
cd -
