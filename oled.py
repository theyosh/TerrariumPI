import gettext
gettext.install('terrariumpi', 'locales/')

from hardware.display import terrariumDisplay

print(terrariumDisplay.available_displays)

oled = terrariumDisplay(None, 'SSD1306', '3c')
print(oled)
print(dir(oled))

#oled.write_image('/home/pi/TerrariumPI/static/assets/img/profile_image.jpg')

oled.message('Dit is een test bericht met een hele lange regel.....\nDit is\neen test\nbericht met een hele\nlange regel.....\nDit is een test bericht met een hele lange regel.....')