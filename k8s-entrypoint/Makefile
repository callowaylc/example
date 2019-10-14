export NS ?= test
export NAME ?= examplejob
export JOBID := $(shell uuidgen || cat /proc/sys/kernel/random/uuid)
export TS := $(shell date +%s)
VERSION := 2.7-alpine
CTX := docker-desktop

.PHONY: make run
.SILENT: -

make:
	docker pull python:$(VERSION)
	- kubectl create namespace $(NS) 2>/dev/null || true
	- kubectl config set-context $(CTX) --namespace $(NS)

run:
	cat manifest.yaml \
		| kubectl delete -f - ||:

	cat ./manifest.yaml \
		| tee /dev/stderr \
		| envsubst \
		| kubectl apply -f - \
				-n $(NS)

