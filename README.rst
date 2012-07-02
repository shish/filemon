filemon
~~~~~~~
See what processes are making use of a given file

example:
--------
$ filemon.py /home/media/video.avi

Open the video in a video player. Filemon outputs:

::
    13:32:51,507 INFO  [root] ['/usr/bin/mplayer']: /home/media/video.avi: IN_OPEN
    13:32:51,600 INFO  [root] ['/usr/bin/mplayer', '/usr/bin/mplayer']: /home/media/video.avi: IN_ACCESS
    13:32:51,969 INFO  [root] ['/usr/bin/mplayer', '/usr/bin/mplayer']: /home/media/video.avi: IN_ACCESS
    13:32:52,977 INFO  [root] []: /home/media/video.avi: IN_ACCESS
    13:32:53,110 INFO  [root] []: /home/media/video.avi: IN_CLOSE_NOWRITE

Note that the last two entries don't have a process - this is because filemon
can only look at the list of which processes have a file *currently open*, so
if the file is being closed, renamed, or is a small file that is written then
closed very quickly, it won't still be open by the time filemon checks.

Since the inotify API doesn't list give the PID of the process performing the
action, this unreliable guessing method seems to be the best option. It's
still a terrible option though :-(
