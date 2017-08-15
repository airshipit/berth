#!/bin/bash

set -ex

NS=berth

helm install --name=berth --debug ./berth --values=examples/cirros-test.yaml --namespace="${NS}"

# wait until we get a PODIP
while : ; do
    PODIP=$(kubectl -n "${NS}" get pods -o wide -o json | jq -r '.items[].status.podIP')
    if [ -n "$PODIP" -a "null" != "$PODIP" ] ; then
	break
    fi
    echo "waiting for PODIP"
    # XXX
    kubectl get pods --all-namespaces
    sleep 2
done

kubectl -n "${NS}" get pods

# wait for pod to come up say something on ssh
timeout=60
t=0
while : ; do
    if echo "bye" | nc "${PODIP}" 22 | grep --quiet ^SSH ; then
        echo "VM up"
	break
    fi
    if [ $t -gt $timeout ] ; then
        exit 2
    fi
    t=$(($t + 5))
    sleep 2
done

# verify we can cleanup
helm upgrade berth ./berth --values=berth/values.yaml

helm delete --purge berth
