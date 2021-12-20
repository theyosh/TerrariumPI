IMAGE=theyosh/terrariumpi
VERSION=4.1.0

.PHONY: all build run logs

all: build

build:
	docker buildx build \
		--progress=plain \
		--platform linux/arm/v7 \
		-t $(IMAGE):$(VERSION) \
		-f Dockerfile \
		.

run: build
	docker-compose down; docker-compose up -d

logs:
	docker-compose logs -f
