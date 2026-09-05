#!/vendor/bin/sh

SETTING=is_enable_esim_for_user

[ "$(/system/bin/cmd settings get secure $SETTING)" = "null" ] || exit 0

exec /system/bin/cmd settings put secure $SETTING 1
