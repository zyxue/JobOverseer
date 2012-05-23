#! /usr/bin/env python

"""This script is used to filter the jobids with regex against job names"""

import re
import xml.dom.minidom as xdm

def guillimin_jidfilter(raw_xml_data, filter):
    xml_data = xdm.parseString(raw_xml_data)

    jids_jns = []	      # list used to collect a list of [jobid, jobname]
    queues = xml_data.getElementsByTagName("queue")
    for queue in queues:
	for job in queue.getElementsByTagName('job'):
	    jn = job.getAttribute('JobName')
	    match = re.search(filter, jn)
	    if match:
		jids_jns.append([job.getAttribute('JobID'), jn])
    return jids_jns

def scinet_jidfilter(raw_xml_data, filter):
    pass

def mp2_jidfilter(raw_xml_data, filter):
    pass

def colosse_jidfilter(raw_xml_data, filter):
    pass

def lattice_jidfilter(raw_xml_data, filter):
    pass

def orca_jidfilter(raw_xml_data, filter):
    pass

def nestor_jidfilter(raw_xml_data, filter):
    pass
