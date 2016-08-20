# See the README for installation instructions.
UGLIFY = node_modules/.bin/uglifyjs

all: \
	$(shell npm install) \
	dist/Leaflet.fullscreen.min.js \

clean:
	rm -f dist/Leaflet.fullscreen.min.js

dist/Leaflet.fullscreen.min.js: dist/Leaflet.fullscreen.js
	$(UGLIFY) dist/Leaflet.fullscreen.js > dist/Leaflet.fullscreen.min.js

.PHONY: clean
