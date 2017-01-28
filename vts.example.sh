#! /bin/sh

### BEGIN INIT INFO
# Provides:          vts
# Required-Start:    $network $local_fs $syslog
# Required-Stop:     $local_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: VK to Slack
# Description: Bot, which spy vk topic and he posted to slack
### END INIT INFO

. /lib/lsb/init-functions

case "$1" in
    start)
        cd /path/to/vts
        if [ -f vts.py ]
	    then
            python vts.py
	    fi
	    ;;
    stop|reload|restart|force-reload|status)
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|force-reload|status}" >&2
        exit 1
        ;;
esac

exit 0