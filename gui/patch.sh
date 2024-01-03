#!/bin/bash

# Patch wrong .scss files: https://github.com/ColorlibHQ/AdminLTE/issues/4255
sed -i 's@\&\.bg-#{$name} {@#{if\(\&, "\&.bg-#{\$name}",".bg-#{\$name}"\)} {@' node_modules/admin-lte/build/scss/mixins/*

# Bootstrap old abs() function fix
sed -i 's@  $dividend: abs($dividend);@  $dividend: math.abs($dividend);@' node_modules/bootstrap/scss/vendor/_rfs.scss