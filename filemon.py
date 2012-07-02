#!/usr/bin/python

#
# Filemon (c) Shish <webmaster@shishnet.org> 2012
#
# Consider this code proof-of-concept, licensed as public domain for now
#

import sys
import logging
from glob import glob
import os

from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes


def getusers(path):
    users = []
    for fullfd in glob("/proc/*/fd/*"):
        try:
            openpath = os.readlink(fullfd)
            _root, _proc, pid, _fd, fd = fullfd.split("/")
            if os.readlink(fullfd) == path:
                users.append(os.readlink("/proc/%s/exe" % pid))
        except OSError as e:
            pass
    return users


def main(argv):
    if len(argv) == 1:
        print "Usage: %s [file]" % argv[0]
        return 1

    path = argv[1]

    logging.basicConfig(
        level    = logging.DEBUG,
        format   = "%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s",
        datefmt  = "%H:%M:%S",
        filename = None
        #filename = "/tmp/filemon.log"
    )

    logging.debug("Init Watcher (%s)" % path)
    class PClose(ProcessEvent):
        def process_default(self, event):
            logging.info("%s: %s: %s" % (getusers(event.pathname), event.pathname, str(event.maskname)))

    wm = WatchManager()
    notifier = Notifier(wm, PClose())
    wm.add_watch(path, EventsCodes.ALL_FLAGS['ALL_EVENTS'], rec=True)

    logging.info("Waiting for updates")
    while True:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
