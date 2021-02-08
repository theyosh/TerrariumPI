#!/bin/bash

FILES="views/*.html views/api/*.html views/includes/*.html views/layouts/*.html views/modals/*.html *.py"

cd ..
pygettext -k N_ -v -a -n -o locales/terrariumpi.pot ${FILES}

for translation in `grep -r -h -o -e "_('[^)]\+')" ${FILES} | sort | uniq | sed "s/\\\\\'/\\'/g" | sed "s/ /%20/g" `; do
  translation=${translation:3:-2}
  translation=${translation//\%20/ }
  if [ `grep -c -F "\"${translation}\"" locales/terrariumpi.pot` -eq 0 ]; then
    echo "Adding missing ${translation}"
    echo "#: Missing text string" >> locales/terrariumpi.pot
    echo "msgid \"${translation}\"" >> locales/terrariumpi.pot
    echo "msgstr \"\"" >> locales/terrariumpi.pot
    echo "" >> locales/terrariumpi.pot
  fi
done

VERSION=`grep ^__version__ "terrariumPI.py" | cut -d' ' -f 3`
VERSION="${VERSION//\'/}"
YEAR=`date "+%Y"`
NOW=`date "+%Y-%m-%d %H:%M%z"`

sed -e "s@YEAR ORGANIZATION@2016-${YEAR} TheYOSH@g" \
    -e "s@FIRST AUTHOR <EMAIL\@ADDRESS>, YEAR@Joshua (TheYOSH) Rubingh, <terrariumpi\@theyosh.nl>, 2016-${YEAR}@g" \
    -e "s@PACKAGE VERSION@TerrariumPI ${VERSION}@g" \
    -e 's@CHARSET@UTF-8@g' \
    -e 's@ENCODING@8bit@g' \
    -i locales/terrariumpi.pot

echo "Done!"

cd -