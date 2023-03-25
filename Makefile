IMAGE ?= theyosh/terrariumpi
VERSION ?= $(shell grep -E "__version__ = '(.*)'" terrariumPI.py | grep -Po [0-9\.]+)
GITHUB_SHA ?= $(shell git rev-parse HEAD)


.PHONY: all build run logs gui docs

all: build push

build:
	docker run --privileged docker/binfmt:a7996909642ee92942dcd6cff44b9b95f08dad64
	docker buildx build \
		--progress=plain \
		--platform linux/arm/v7 \
		-t $(IMAGE):$(VERSION) \
		--build-arg GITHUB_SHA=${GITHUB_SHA} \
		-f Dockerfile \
		.

push:
	docker run --privileged docker/binfmt:a7996909642ee92942dcd6cff44b9b95f08dad64
	GITHUB_SHA=${GITHUB_SHA} docker buildx build \
		--progress=plain \
		--platform linux/arm/v7 \
		-t $(IMAGE):$(VERSION) \
		--build-arg GITHUB_SHA=${GITHUB_SHA} \
		-f Dockerfile \
		--push \
		.

run: build restart

restart:
	docker-compose down; docker-compose up -d
	sleep 30 # Wait for it to come up
	$(MAKE) logs

logs:
	docker-compose logs -f

gui:
	npm install
	npm run build

docs:
	bundle install
	cd docs && jekyll serve
