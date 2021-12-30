IMAGE ?= theyosh/terrariumpi
VERSION ?= $(shell grep -E "__version__ = '(.*)'" terrariumPI.py | grep -Po [0-9\.]+)

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
	$(MAKE) logs

logs:
	docker-compose logs -f
