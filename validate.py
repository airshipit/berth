#!/usr/bin/python
#
# Ideally we would use jsonschema.validate but getting useful error
# output has been challenging.  This can be revisited as needed.

import yaml
import sys

def validate_leaves(prefix, vm, l):
    valid_leaves = [ ]

    # first check to make sure we have what we think we should
    for nd in l:
        n = nd[0]
        t = nd[1]
        o = False
        if len(nd)>2:
            o = nd[2]
        try:
            if n not in vm.keys():
                if o:
                    print "[W] Missing leaf:", prefix+n
                else:
                    print "[E] Missing leaf:", prefix+n
                continue
            if type(vm[n]) != type(t):
                print "[E] Wrong type for %s (got '%s' expected '%s')" % (prefix+n, type(vm[n]).__name__, type(t).__name__)
                continue
        except:
            print "[W] Unable to validate leaf:", prefix+n
            continue

        valid_leaves.append(n)

    if type(vm) == type(dict()):
        # now look for things we don't know how to deal with
        for n in vm.keys():
            if n not in [ x[0]  for x in l]:
                print "[W] Unexpected leaf:", prefix+n

    return valid_leaves

def validate_file(filename):
    try:
        yamlgen = list(yaml.safe_load_all(open(filename)))
    except yaml.parser.ParserError:
        print "[E] Invalid yaml"
        return

    if not yamlgen or not yamlgen[0]:
        print "[E] File contains no valid yaml"
        return
    top = list(yamlgen)[0]

    vmlist = top["vmlist"]
    if not vmlist  or  not isinstance(vmlist, dict):
        print "[E] No vmlist dict declared"
        return

    for name in vmlist:
        vm = vmlist[name]
        print "VM:", name

        vl = validate_leaves("", vm, [ ("enabled",bool()), ("vmconfig",dict()), ("netconfig",dict()), ("cloudconfig",dict()) ] )
        if "vmconfig" in vl:
            # validate vmconfig
            vmconfig = vm["vmconfig"]
            vl2 = validate_leaves("vmconfig.", vmconfig, [ ("cpu",dict()), ("rootfs",dict()) ])

            if "cpu" in vl2:
                # validate vmconfig.cpu
                cpu = vmconfig["cpu"]
                vl3 = validate_leaves("vmconfig.cpu.", cpu, [ ("vcpu",int()), ("ram_mb",int()) ])
                if "vcpus" in vl3:
                    vcpu = int(cpu["vcpus"])
                    if vcpu < 1  or  vcpu > 8:
                        print "[W] vmconfig.cpu.vcpu has odd looking value:", vcpu
                if "ram_mb" in vl3:
                    ram_mb = int(cpu["ram_mb"])
                    if ram_mb < 512   or   ram_mb > 32768:
                        print "[W] vmconfig.cpu.ram_mb has odd looking value:", ram_mb

            if "rootfs" in vl2:
                # validate vmconfig.rootfs
                rootfs = vmconfig["rootfs"]
                vl3 = validate_leaves("vmconfig.rootfs.", rootfs, [ ("sourceurl",str()), ("localtarget",str()), ("pvc_size",str()), ("pvc_class",str(), True) ])

                if "sourceurl" in vl3:
                    if not rootfs["sourceurl"].startswith("http"):
                        print "[W] vmconfig.rootfs.sourceurl has odd looking value:", rootfs["sourceurl"]

        if "netconfig" in vl:
            # validate netconfig
            netconfig = vm["netconfig"]
            vm2 = validate_leaves("netconfig.", netconfig, [ ("ports",dict()), ("readinessTcpProbe",int(), True) ])
            # do more?

        if "cloudconfig" in vl:
            # validate cloudconfig
            cloudconfig = vm["cloudconfig"]
            vl2 = validate_leaves("cloudconfig.", cloudconfig, [ ("metadata",str()), ("userdata",str()) ])

            # check things look sane
            for yamlobj in [ "metadata", "userdata" ]:
                if yamlobj in vl2:
                    try:
                        yaml.load(cloudconfig[yamlobj])
                    except:
                        print "[E] Bad yaml for vmconfig.cloudconfig.%s" % yamlobj


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        print "Filename:", fn
        validate_file(fn)
        print
