IMAGE ?= theyosh/terrariumpi
VERSION ?= 4.1.0

.PHONY: all build run logs

all: build

build:
	docker buildx build \
		--progress=plain \
		--platform linux/arm/v7 \
		-t $(IMAGE):$(VERSION) \
		-f Dockerfile \
		.

run: build restart

restart:
	docker-compose down; docker-compose up -d
	sleep 30 # Wait for it to come up
	$(MAKE) scan
	$(MAKE) logs

logs:
	docker-compose logs -f

scan:
	curl \
		--retry 30 \
		--retry-connrefused \
		'http://localhost:8090/api/sensors/scan/' \
		-X POST \
		-H 'Accept: application/json, text/javascript, */*; q=0.01' \
		-H 'Accept-Language: en-US,en;q=0.5' \
		-H 'Accept-Encoding: gzip, deflate' \
		-H 'Content-Type: application/json;charset=UTF-8' \
		-H 'Origin: http://localhost:8090' \
		-H 'Referer: http://localhost:8090/' \
		--data-raw '{}' \
