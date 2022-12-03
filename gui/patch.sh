#!/bin/bash

# Patch wrong .scss files: https://github.com/ColorlibHQ/AdminLTE/issues/4255
sed -i 's@\&\.bg-#{$name} {@#{if\(\&, "\&.bg-#{\$name}",".bg-#{\$name}"\)} {@' node_modules/admin-lte/build/scss/mixins/*
