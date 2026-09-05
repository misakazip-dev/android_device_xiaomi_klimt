#!/vendor/bin/sh

# Mobile FeliCa runs on the embedded secure element (felica/common.cfg selects
# eSE1) and only the JP SKU is provisioned for it, so hide it everywhere else.
#
# Only ever act before the setup wizard has finished. Past that point whatever
# state these packages are in is the user's choice, and re-applying this on every
# boot would keep undoing it.
[ "$(/system/bin/cmd settings get global device_provisioned)" = "1" ] && exit 0

# ro.boot.hwc comes from the bootloader and is the same value the NFC HAL's
# is_felica_support() keys on when it decides whether to load the JP RF
# configuration, so gate on it too rather than on anything the build could get
# wrong.
[ "$(/system/bin/getprop ro.boot.hwc)" = "JP" ] && exit 0

for pkg in com.felicanetworks.mfc \
           com.felicanetworks.mfm.main \
           com.felicanetworks.mfs \
           com.felicanetworks.mfw.a.boot; do
    /system/bin/cmd package disable-user --user 0 "$pkg"
done
