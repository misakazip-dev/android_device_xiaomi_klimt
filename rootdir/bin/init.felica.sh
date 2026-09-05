#!/vendor/bin/sh

# This is a script to enable Osaifu-Keitai on JP devices only.
[ "$(/system/bin/getprop ro.boot.hwc)" = "JP" ] && exit 0

for pkg in com.felicanetworks.mfc \
           com.felicanetworks.mfm.main \
           com.felicanetworks.mfs \
           com.felicanetworks.mfw.a.boot; do
    /system/bin/cmd package disable-user --user 0 "$pkg"
done
