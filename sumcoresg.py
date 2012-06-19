#!/usr/bin/env python

import os

import miscell

def main():
    """sum cores usage for the group"""
    cluster = miscell.gen_cluster_obj(os.environ['HOSTNAME'])
    usermap = miscell.user_mapping()
    cluster.report_to_me(usermap)

if __name__ == "__main__":
    main()
