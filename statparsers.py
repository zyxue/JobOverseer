#! /usr/bin/env python

import xml.etree.ElementTree as xml

def scinet_statparser(raw_data, userhash, cores_per_node):
    raw_data = xml.fromstring(raw_data)

    active_cores, total_cores = 0, 0
    rcu, qcu = init_cu(userhash)

    queues = raw_data.findall('queue')
    for queue in queues:
        for job in queue.findall('job'):
            # collect global statitics
            # RegNodes seems to be set by None always after checking with set 
            cores = int(job.get('ReqProcs'))
            job_state = job.get('State')
            if job_state == 'Running':
                active_cores += cores
            total_cores += cores

            # collect statistics for my group
            job_owner = job.get('User')
            if job_owner in userhash:
                realname = userhash[job_owner]
                if job_state == 'Running':
                    rcu[realname] += cores
                else:
                    qcu[realname] += cores
            
    display_active_usage(active_cores, total_cores)

    return rcu, qcu

def mp2_statparser(raw_data, userhash, cores_per_node):
    raw_data = xml.fromstring(raw_data)
    # raw_data = xml.fromstring(result.translate(None, "&")) 
    # the above line is from cing

    total_cores = sum([int(job.find('Resource_List').find("nodes").text.split(':')[0]) for job in raw_data])
    active_cores = sum([int(job.find('Resource_List').find("nodes").text.split(':')[0]) for job in raw_data if job.find('job_state').text == 'R'])

    rcu, qcu = init_cu(userhash)
    for job in raw_data:
        # e.g. 'xuezhuyi@ip13.m'
        job_owner = job.find('Job_Owner').text.split('@')[0]
        if job_owner in userhash:                          # user in my group
            realname = userhash[job_owner]
            # e.g. 1:ppn=1
            cores = cores_per_node * int(job.find('Resource_List').find("nodes").text.split(':')[0])

            # possible jobs status set(['Q', 'H', 'R'])
            job_state = job.find('job_state').text
            if job_state == 'R':
                rcu[realname] += cores
            else:
                qcu[realname] += cores

    display_active_usage(active_cores, total_cores)
    return rcu, qcu


def init_cu(userhash):
    rcu = {}                    # collect cores usage by running jobs
    qcu = {}                    # collect cores usage by queueing cores
    for d in [rcu, qcu]:
        for n in set(userhash.values()):
            d[n] = 0
    return rcu, qcu

def display_active_usage(active_cores, total_cores):
    print "=" * 44
    print "Active cores {0} / {1} = {2:.2%}".format(active_cores, total_cores, 
                                                active_cores / float(total_cores))
    print 
    print "THIS NUMBER IS NOT ACURATE ON mp2, scinet" 
    print "=" * 44
    print 
