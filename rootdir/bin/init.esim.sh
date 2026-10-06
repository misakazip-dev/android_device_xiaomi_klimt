#!/vendor/bin/sh
#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Only the Japanese hardware SKU may operate the eUICC.
if [ "$(getprop ro.boot.hwc)" != "JP" ]; then
    setprop vendor.esim.state disabled
    exit 0
fi

case "$1" in
    enable) /vendor/bin/mtkmtb -c 5:1 ;;
    disable) /vendor/bin/mtkmtb -c 5:2 ;;
    "") ;;
    *) exit 1 ;;
esac

# Do not report a modem error or an empty response as an enabled eUICC.
if result=$(/vendor/bin/mtkmtb -c 5:3 2>&1); then
    if printf '%s\n' "$result" | grep -Eq 'eID=[0-9]{32}([^0-9]|$)'; then
        setprop vendor.esim.state enabled
        exit 0
    fi
fi
setprop vendor.esim.state disabled
