#! /usr/bin/env python

import os
import miscell
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', dest='filter', default=None, required=True,
			help="the regex needed to identify those jobs you wanna cancel")
    args = parser.parse_args()
    return args

def main():
    """sum cores usage for the group"""
    args = parse_cmd()
    cluster = miscell.identify_cluster(os.environ['HOSTNAME'])
    cluster.canceljobs(args.filter)

if __name__ == "__main__":
    main()

