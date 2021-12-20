IMAGE=cnelson/terrariumpi
VERSION=4.1.0

.PHONY: all build run logs

all: build

build:
	sudo docker buildx build \
		--progress=plain \
		--platform linux/arm/v7 \
		-t $(IMAGE):$(VERSION) \
		-f Dockerfile \
		.

run: build
	cd /media/external/runtime; sudo docker-compose down; sudo docker-compose up -d

logs:
	cd /media/external/runtime; sudo docker-compose logs -f
