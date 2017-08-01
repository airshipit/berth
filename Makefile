# This Makefile is used during development and can usually be ignored
# by most people.

all: test

default: test

test: install

install: build
	@echo
	-helm delete --purge berth >>helm.log 2>&1
	@echo
	@[ -f override.yaml ] || touch override.yaml
	helm install ./berth-0.1.0.tgz --values=override.yaml --name=berth >>helm.log 2>&1
	@sleep 5.0 # give k8s a chance to see the IP
	@echo
	kubectl get pods -o wide

build:
	@echo
	helm lint berth
	@echo
	helm package berth

clean:
	rm -f berth-0.1.0.tgz helm.log

.PHONY:
	all default build clean
