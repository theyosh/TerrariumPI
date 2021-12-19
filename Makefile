IMAGE=cnelson/terrariumpi
VERSION=4.1.0

.PHONY: all terrariumpi

all: terrariumpi

terrariumpi:
	sudo docker buildx build --platform linux/arm/v7 -t $(IMAGE):$(VERSION) -f Dockerfile .

