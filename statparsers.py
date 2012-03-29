#! /usr/bin/env python

import xml.etree.ElementTree as xml

def scinet_statparser(raw_data, userhash, cores_per_node):
    pass

def mp2_statparser(raw_data, userhash, cores_per_node):
    raw_data = xml.fromstring(raw_data)
    # raw_data = xml.fromstring(result.translate(None, "&")) 
    # the above line is from cing

    r_cores = {}                    # collect cores used by running jobs
    q_cores = {}                    # collect cores requested by queueing cores

    total_cores = sum([int(job.find('Resource_List').find("nodes").text.split(':')[0]) for job in raw_data])
    active_cores = sum([int(job.find('Resource_List').find("nodes").text.split(':')[0]) for job in raw_data if job.find('job_state').text == 'R'])

    print "=" * 44
    print "Active cores {0} / {1} = {2:.2%}".format(active_cores, total_cores, 
                                                active_cores / float(total_cores))
    print 
    print "THIS NUMBER IS NOT ACURATE ON mp2" 
    print "=" * 44
    print 

    for job in raw_data:
        # e.g. 'xuezhuyi@ip13.m'
        job_owner = job.find('Job_Owner').text.split('@')[0]
        if job_owner in userhash:                          # user in my group
            # initialize dictionary if first time
            realname = userhash[job_owner]
            for d in [r_cores, q_cores]:
                if realname not in d:
                    d[realname] = 0

            # e.g. 1:ppn=1
            cores = cores_per_node * int(job.find('Resource_List').find("nodes").text.split(':')[0])

            # possible jobs status set(['Q', 'H', 'R'])
            job_state = job.find('job_state').text
            if job_state == 'R':
                r_cores[realname] += cores
            else:
                q_cores[realname] += cores

    return r_cores, q_cores

