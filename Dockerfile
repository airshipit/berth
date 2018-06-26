ARG FROM=ubuntu:16.04
FROM ${FROM}

LABEL org.opencontainers.image.authors='airship-discuss@lists.airshipit.org, irc://#airshipit@freenode'
LABEL org.opencontainers.image.url='https://airshipit.org'
LABEL org.opencontainers.image.documentation='https://airship-berth.readthedocs.org'
LABEL org.opencontainers.image.source='https://git.openstack.org/openstack/airship-berth'
LABEL org.opencontainers.image.vendor='The Airship Authors'
LABEL org.opencontainers.image.licenses='Apache-2.0'

RUN apt-get update && apt-get install -y qemu-kvm dnsmasq bridge-utils mkisofs curl jq wget iptables
RUN apt-get clean
RUN rm -f /var/lib/apt/lists/* || true

ENTRYPOINT ["/bin/sleep", "infinity"]

VOLUME "/image"
EXPOSE 22
CMD []
