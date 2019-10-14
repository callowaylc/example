export NAME ?= example
export JOBID := $(shell uuidgen || cat /proc/sys/kernel/random/uuid)
export EPOCH := $(shell date +%s)
VERSION := 2.7-alpine

.PHONY: make install
.SILENT: -

make:
	helm lint .
	docker pull python:$(VERSION)

debug:
	helm upgrade $(NAME) . \
	  --force \
	  --install \
	  --set "jobid=$(JOBID)" \
	  --set "epoch=$(EPOCH)" \
	  --dry-run \
	  --debug


install:
	helm upgrade $(NAME) . \
	  --force \
	  --install \
	  --set "jobid=$(JOBID)" \
	  --set "epoch=$(EPOCH)"

clean:
	k delete pods,jobs,cronjobs --all
