# This Makefile is used during development and can usually be ignored
# by most people.

default:
	@echo Useful valid targets are test-validate, test-install, test-uninstall

all: test-validate test-install test-uninstall

test-validate:
	@echo ===========================================================================
	python validate.py examples/*
	@echo ===========================================================================


test-install: build
	@echo
	-helm delete --purge berth
	@echo
	helm install --name=berth --debug ./berth
	helm upgrade --debug berth ./berth \
			--values examples/cirros-test.yaml \
			--values examples/demo-ub14-apache.yaml \
			--values examples/ub16-smp-test.yaml
	@sleep 5 # give k8s a chance to see the IP
	@echo
	kubectl get pods -o wide

test-uninstall:
	helm delete --purge berth

build:
	@echo
	helm lint berth

clean:
	rm -f *~ */*~ */*/*~ berth-0.1.0.tgz
	rm -rf docs/build

.PHONY: docs
docs: clean build_docs

.PHONY: build_docs
build_docs:
	tox -e docs

.PHONY:
	all default build clean test-validate test-install test-uninstall
