FROM ubuntu:16.04

RUN apt-get update && apt-get install -y qemu-kvm dnsmasq bridge-utils mkisofs curl jq wget iptables
RUN apt-get clean
RUN rm -f /var/lib/apt/lists/* || true

ENTRYPOINT ["/bin/sleep", "infinity"]

VOLUME "/image"
EXPOSE 22
CMD []
