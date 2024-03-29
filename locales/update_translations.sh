#!/bin/bash

FILES="*.py"

cd ..
pygettext -k N_ -v -a -n -o locales/terrariumpi.pot ${FILES}

for translation in $(grep -r -h -o -e "N\?_(\('\|\"\)[^)]\+\('\|\"\))" ${FILES} | sort | uniq | sed "s/\\\\\'/\\'/g" | sed "s/ /%20/g" ); do
  translation="${translation:3:-2}"
  translation="${translation//\%20/ }"
  if [ "${translation:0:1}" = "'" ]; then
    translation=${translation:1}
  fi
  translation="${translation//\\\'/\'}"

  if [ $(grep -c -F "\"${translation}\"" locales/terrariumpi.pot) -eq 0 ]; then
    echo "Adding missing text '${translation}'"

    locations="#: "
    IFS=$'\n'
    for filename in $(grep -r -n -o "_('${translation}')" ./*.py | sort) ; do
      filename=${filename/:_(\'${translation}\')/}
      locations="${locations} ${filename}"
    done
    IFS=' '

    echo "${locations}" >> locales/terrariumpi.pot
    echo "msgid \"${translation}\"" >> locales/terrariumpi.pot
    echo "msgstr \"\"" >> locales/terrariumpi.pot
    echo "" >> locales/terrariumpi.pot
  fi
done

VERSION=$(grep ^__version__ "terrariumPI.py" | cut -d' ' -f 3)
VERSION="${VERSION//\'/}"
YEAR=$(date "+%Y")

sed -e "s@YEAR ORGANIZATION@2016-${YEAR} TheYOSH@g" \
    -e "s@FIRST AUTHOR <EMAIL\@ADDRESS>, YEAR@Joshua (TheYOSH) Rubingh, <terrariumpi\@theyosh.nl>, 2016-${YEAR}@g" \
    -e "s@PACKAGE VERSION@TerrariumPI ${VERSION}@g" \
    -e 's@CHARSET@UTF-8@g' \
    -e 's@ENCODING@8bit@g' \
    -i locales/terrariumpi.pot

echo "Done!"

cd -
