#!/vendor/bin/sh

/system/bin/logcat -b all -v threadtime -f /metadata/klimt-logcat.log &
exec /system/bin/dmesg -w > /metadata/klimt-dmesg.log 2>&1
