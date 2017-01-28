#! /bin/sh

### BEGIN INIT INFO
# Provides:          vts
# Required-Start:    $all
# Required-Stop:     $network $named $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: VK to Slack
# Description: Bot, which spy vk topic and he posted to slack
### END INIT INFO

. /lib/lsb/init-functions

cd /path/to/vts

do_start() {
    python vts.py start
    log_daemon_msg "Started VTS" "vts"
}

do_stop() {
    python vts.py stop
    log_daemon_msg "Stopping VTS" "vts"
}

case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        do_start
        ;;
    reload|force-reload|status)
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|force-reload|status}" >&2
        exit 1
        ;;
esac

exit 0