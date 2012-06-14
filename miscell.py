#! /usr/bin/env python

import os
import xml.dom.minidom as xdm

import clusters

def identify_cluster(hostname):
    # I should find a way to identify the location of clusters.xml,
    # clusters.xml should be rewritten using more of attributes based on the
    # xml from statcmd

    dom = xdm.parse(os.path.join(os.path.dirname(__file__), 'clusters.xml'))
    hns_nodes = dom.getElementsByTagName("hostnames") # hn: hostname
    for node in hns_nodes:
	hns = [i.childNodes[0].data for i in node.getElementsByTagName("hn")]
	if hostname in hns:
	    c =  node.parentNode
	    args = [ c.getElementsByTagName(tag)[0].childNodes[0].data
		     for tag in ['clustername', 'cores-per-node', 'statcmd']
		     ]
	    cluster_obj = clusters.Cluster(*args)
	    return cluster_obj

def user_mapping():
    dom = xdm.parse(os.path.join(os.path.dirname(__file__), 'users.xml'))
    users = dom.getElementsByTagName('username')
    return {u.childNodes[0].data: u.nextSibling.childNodes[0].data for u in users}

if __name__ == "__main__":
    from pprint import pprint as pp

    hostname = os.environ['HOSTNAME']	# hn: hostname
    pp(identify_cluster(hostname))
    pp(user_mapping())
