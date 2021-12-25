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
