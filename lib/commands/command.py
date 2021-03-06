#!/usr/bin/env python3

import logging
import os
import re
import subprocess
import threading
import datetime

from optparse import OptionParser

ignore_patterns = {
    'consul': lambda v: re.search(r'-(alpha|beta|rc|)|\+ent', v),
    'flutter': lambda v: re.search(r'-dev|pre', v),
    'golang': lambda v: re.search(r'beta|rc', v),
    'kubectl': lambda v: re.search(r'alpha|rc', v),
    'python': lambda v: not re.match(r'^\d', v) or re.search(r'a|b|dev|rc', v),
    'ruby': lambda v: not re.match(r'^\d', v) or re.search(r'-dev|-preview', v),
    'tmux': lambda v: re.search(r'rc', v),
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_tool_versions():
    tuples = []
    with open(os.path.expanduser('~/.tool-versions')) as f:
        for line in f.readlines():
            splited = re.split('\s+', line.strip())
            plugin, versions = splited[0], splited[1:]
            tuples.append((plugin, versions))
    return tuples

def check_version(options, plugin, versions):
    logging.debug(f'check {plugin}')

    sp = subprocess.Popen(['asdf', 'list', 'all', plugin], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _stderr = sp.communicate()

    newer_versions = [line.strip() for line in stdout.decode('utf-8').split('\n') if line.strip()]
    logging.debug(f'{plugin}: found {newer_versions}')

    if plugin in ignore_patterns.keys():
        fn = ignore_patterns[plugin]

        ignored = [v for v in newer_versions if fn(v)]
        logging.debug(f'{plugin}: ignore {ignored}')

        newer_versions = [v for v in newer_versions if v not in ignored]
        logging.debug(f'{plugin}: preserve {newer_versions}')

    if not newer_versions:
        print(f'{plugin}: {bcolors.WARNING}no latest version{bcolors.ENDC}')
        return

    latest_version = newer_versions[-1]
    if latest_version in versions:
        print(f'{plugin}: {bcolors.OKGREEN}up-to-date{bcolors.ENDC}')
    else:
        print(f'{plugin}: {bcolors.FAIL}{latest_version} <- {",".join(versions)}{bcolors.ENDC}')

def main():
    parser = OptionParser()
    parser.add_option('-v', '--verbose', help='Verbose', action='store_true')
    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    tuples = read_tool_versions()

    # filter plugins if positional arguments are given
    if args:
        tuples = [t for t in tuples if t[0] in args]

    plugins = set([t[0] for t in tuples])

    threads = []

    for t in tuples:
        plugin, versions = t

        th = threading.Thread(target=check_version, args=(options,plugin,versions,))
        th.start()

        threads.append(th)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
