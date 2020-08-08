#!/bin/bash

cd ..
mv views/inc/footer.tpl views/inc/footer.tpl_tmp
pygettext -v -a -n -o locales/terrariumpi.pot views/*.tpl views/inc/*.tpl *.py
mv views/inc/footer.tpl_tmp views/inc/footer.tpl
cd -

for translation in `grep -r -h -o -e "_('[^)]\+')" ../views/*.tpl ../views/inc/*.tpl ../static/js/terrariumpi.js ../*.py | sort | uniq | sed "s/\\\\\'/\\'/g" | sed "s/ /%20/g" `; do
  translation=${translation:3:-2}
  translation=${translation//\%20/ }
  if [ `grep -c -F "\"${translation}\"" terrariumpi.pot` -eq 0 ]; then
    echo "Adding missing ${translation}"
    echo "#: Missing text string" >> terrariumpi.pot
    echo "msgid \"${translation}\"" >> terrariumpi.pot
    echo "msgstr \"\"" >> terrariumpi.pot
    echo "" >> terrariumpi.pot
  fi
done

# Add static translations
echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Sensor temperature\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Sensor humidity\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Sensor distance\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Sensor ph\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Sensor settings\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Switch status\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Switch settings\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Door settings\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Webcam settings\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"Audio files\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"System status\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"System log\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"System environment\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

echo "#: Missing text string" >> terrariumpi.pot
echo "msgid \"System settings\"" >> terrariumpi.pot
echo "msgstr \"\"" >> terrariumpi.pot
echo "" >> terrariumpi.pot

VERSION=`grep "version = " ../defaults.cfg | grep -o -E "[0-9\.]+"`
YEAR=`date "+%Y"`
NOW=`date "+%Y-%m-%d %H:%M%z"`

sed -e "s@YEAR ORGANIZATION@2016-${YEAR} TheYOSH@g" \
    -e "s@FIRST AUTHOR <EMAIL\@ADDRESS>, YEAR@Joshua (TheYOSH) Rubingh, <terrariumpi\@theyosh.nl>, 2016-${YEAR}@g" \
    -e "s@PACKAGE VERSION@TerrariumPI ${VERSION}@g" \
    -e 's@CHARSET@UTF-8@g' \
    -e 's@ENCODING@8bit@g' \
    -i terrariumpi.pot

echo "Done!"
