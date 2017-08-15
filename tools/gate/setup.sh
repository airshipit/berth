#!/bin/sh

set -ex

. /etc/os-release
type=${ID_LIKE:=ID}

if [ "$type" == "debian" ] ; then
    apt-get update
    apt-get install netcat-openbsd jq
else
    yum install netcat jq
fi
