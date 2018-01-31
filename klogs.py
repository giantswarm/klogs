# coding: utf8

# (c) 2017 Giant Swarm GmbH
#
# Licensed under Apache 2.0 license. See LICENSE.

import sys
import json
import argparse
import subprocess


def get_kubectl_logs(selector, namespace="default"):
    """
    Fetch all available log entries for the
    given namespace and selector
    """
    cmd = [
        "kubectl",
        "logs",
        "-n", namespace,
        "-l", selector,
        "--timestamps",
    ]
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            bufsize=1,
                            universal_newlines=True)

    # first run: fetch latest log entries
    while True:
      line = proc.stdout.readline()
      if line != '':
        yield(line.rstrip())
      else:
        break

    # second run: fetch previous log entries
    cmd.append("--previous")
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            bufsize=1,
                            universal_newlines=True)
    while True:
      line = proc.stdout.readline()
      if line != '':
        yield(line.rstrip())
      else:
        break


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse log entries, sort and print them nicely')
    parser.add_argument('-n', '--namespace', dest='namespace', default="default",
                        help='Namespace')
    parser.add_argument('-l', '--selector', dest='selector',
                        help='Pod selector (think kubectl logs -l="<selector>")')
    parser.add_argument('-s', '--stats', dest="stats", action="store_true", help="Print a summary about the log entries")

    args = parser.parse_args()


    # Validate flags
    if args.selector is None:
        sys.stderr.write("Please set a selector using the -l/--selector flag.\n")
        sys.exit(1)

    logentries = []
    for line in get_kubectl_logs(args.selector, args.namespace):

        # split timestamp from the rest
        timestamp, payload = line.split(" ", 1)

        entry = {
            "timestamp": timestamp,
            "entry": payload
        }

        # save our logentry
        logentries.append(entry)


    first_timestamp = None
    last_timestamp = None

    # sort and print logentries
    for entry in sorted(logentries, key=lambda k: k["timestamp"]):

        if first_timestamp == None:
            first_timestamp = entry["timestamp"]
        last_timestamp = entry["timestamp"]

        print("%s %s" % (entry["timestamp"], entry["entry"]))

    if args.stats:
        print("")
        print("%d log entries" % len(logentries))
        print("First entry %s" % first_timestamp)
        print("last entry %s" % last_timestamp)
