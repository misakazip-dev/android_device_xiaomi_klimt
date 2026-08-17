#!/vendor/bin/sh

LOGCAT=/metadata/klimt-logcat.log
DMESG=/metadata/klimt-dmesg.log

/system/bin/grep -q " /metadata " /proc/mounts || exit 1

umask 077
[ -f "$DMESG" ] && /system/bin/mv -f "$DMESG" "$DMESG.previous"

# Keep three 2 MiB logcat windows and one 8 MiB dmesg capture.
/system/bin/logcat -b all -v threadtime -f "$LOGCAT" -r 2048 -n 2 &
ulimit -f 16384
exec /system/bin/dmesg -w > "$DMESG" 2>&1
