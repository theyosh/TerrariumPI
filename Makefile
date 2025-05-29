IMAGE ?= theyosh/terrariumpi
VERSION ?= $(shell grep -E "__version__ = \"(.*)\"" terrariumPI.py | grep -Po [0-9\.]+)
GITHUB_SHA ?= $(shell git rev-parse HEAD)
OS = buster bullseye bookworm

.PHONY: all build run logs gui docs

all: build push

build:
	docker run --privileged tonistiigi/binfmt --install arm
	$(foreach var,$(OS),docker buildx build --progress=plain --network=host --platform linux/arm/v7 -t $(IMAGE):$(VERSION)-${var}      --build-arg GITHUB_SHA=${GITHUB_SHA} -f Dockerfile.${var} .;)

push:
	docker run --privileged tonistiigi/binfmt --install arm
	$(foreach var,$(OS),docker buildx build --progress=plain --network=host --platform linux/arm/v7 -t $(IMAGE):$(VERSION)-${var}      --build-arg GITHUB_SHA=${GITHUB_SHA}                                       -f Dockerfile.${var} --push .;)
	$(foreach var,$(OS),docker buildx build --progress=plain --network=host --platform linux/arm/v7 -t $(IMAGE):$(VERSION)-${var}-java --build-arg GITHUB_SHA=${GITHUB_SHA} --build-arg JAVA=default-jre-headless -f Dockerfile.${var} --push .;)


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
