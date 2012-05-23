import os
import sys
import subprocess

import statparsers
import jidfilters

class Cluster():
    def __init__(self, name, cores_per_node, statcmd):
	"""
	name: name of the cluster
	cores_per_node
	statcmd: the command used to generate usage statics, probably in xml
	"""
        self.name = name
        self.cores_per_node = int(cores_per_node)
        self.statcmd = statcmd
        self.queue_data = None

    def executeCommand(self):
        pipe = subprocess.PIPE
        p = subprocess.Popen(self.statcmd, shell=True, stdout=pipe, stderr=pipe)
        stdout, stderr = p.communicate()
        r = p.returncode
        if r != 0:
            raise ValueError(
                "\ncmd failed: {0}\nstderr: {1}".format(self.statcmd, stderr))
        return stdout

    def report_to_me(self, usermap):
	"""usermap: username-to-realname mapping"""
        raw_xml_data = self.executeCommand()
        dd = {
            'scinet'    : statparsers.scinet_statparser,
            'mp2'       : statparsers.mp2_statparser,
            'guillimin' : statparsers.guillimin_statparser,
            'lattice'   : statparsers.lattice_statparser,
            'orca'      : statparsers.orca_statparser,
            'nestor'   : statparsers.nestor_statparser,
            'colosse'   : statparsers.colosse_statparser,
            }

        # rcu, qcu mean running & queuing core usages
        rcu, qcu = dd[self.name](raw_xml_data, usermap, self.cores_per_node)
        self.display(rcu, qcu, usermap)

    def display(self, rcu, qcu, usermap):
        # result is a tuple
        total_usage = {}
        for realname in set(usermap.values()):
            total_usage[realname] = sum(dd.get(realname, 0) for dd in [rcu, qcu])

        # print title
        print "{0:13s} {1:8s} {2:8s} {3:8s}\n{4:36s}".format(
                'USERNAME', 'Running', 'Queuing', 'TOTAL', "=" * 44)

        # sort by total_usage
        sorted_keys = reversed(sorted(total_usage, key=total_usage.get))

        # print value
        for k in sorted_keys:
            # full name is too long, last name is used, firstname is confusing
            if total_usage[k] != 0:                # don't print results of zero usage
                name = k.split()[0]
                print "{0:13s} {1:<8d} {2:<8d} {3:<8d}".format(
                    name, rcu.get(k, 0), qcu.get(k, 0), total_usage[k])
    def canceljobs(self, filter):
	"""filter should be regular expression"""
        raw_xml_data = self.executeCommand()
        dd = {
            'scinet'    : jidfilters.scinet_jidfilter,
            'mp2'       : jidfilters.mp2_jidfilter,
            'guillimin' : jidfilters.guillimin_jidfilter,
            'lattice'   : jidfilters.lattice_jidfilter,
            'orca'      : jidfilters.orca_jidfilter,
            'nestor'   : jidfilters.nestor_jidfilter,
            'colosse'   : jidfilters.colosse_jidfilter,
            }

	print "=" * 79
	print "{0:^79s}".format("THE SPECIFIED FILTER: " + filter)
	print "=" * 79
        jids_jns = dd[self.name](raw_xml_data, filter)
	# a list of [jobid, jobname]
	# jobname is there for convenient reference
	for [jid, jn] in jids_jns:
	    print "{0:^79s}".format("{0}\t{1}".format(jid, jn))
	    subprocess.call(['canceljob', jid])
