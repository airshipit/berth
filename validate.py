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
    yamlgen = yaml.load_all(open(filename))
    top = [ x  for x in yamlgen ][0]

    vmlist = top["vmlist"]
    index = 0
    for vm in vmlist:
        index += 1
        name = ""
        if "name" in vm:
            name = vm["name"]

        print "Checking:", name, ("(index %d)" % index)

        vl = validate_leaves("", vm, [ ("name",str()), ("enabled",bool()), ("vmconfig",dict()), ("netconfig",dict()), ("cloudconfig",dict()) ] )
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
                vl3 = validate_leaves("vmconfig.rootfs.", rootfs, [ ("sourceurl",str()), ("type_notimpl",str()), ("localtarget",str()), ("pvc_size",str()), ("pvc_class",str(), True) ])

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
            vl2 = validate_leaves("cloudconfig.", cloudconfig, [ ("instance_id",str()), ("metadata",str()), ("userdata",str()) ])

            # check things look sane
            for yamlobj in [ "metadata", "userdata" ]:
                if yamlobj in vl2:
                    try:
                        yaml.load(cloudconfig[yamlobj])
                    except:
                        print "[E] Bad yaml for vmconfig.cloudconfig.%s" % yamlobj

        print "Done"
        print

if __name__ == "__main__":
    for fn in sys.argv[1:]:
        validate_file(fn)
