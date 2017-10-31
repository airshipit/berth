# This Makefile is used during development and can usually be ignored
# by most people.

validation:
	@echo ===========================================================================
	python validate.py example-vmlist-1.yaml
	@echo ===========================================================================
	python validate.py example-vmlist-bad.yaml
	@echo ===========================================================================

all: test

default: test

test: install

install: build
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

build:
	@echo
	helm lint berth

clean:
	rm -f *~ */*~ */*/*~ berth-0.1.0.tgz

.PHONY:
	all default build clean
