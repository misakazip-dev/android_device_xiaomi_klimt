#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# The stock RROs have to land in /vendor/overlay for the overlay manager to pick
# them up. Soong's android_app_import can only install under /vendor/app and the
# build system rejects apks in PRODUCT_COPY_FILES, so they are built here.

LOCAL_PATH := $(call my-dir)

KLIMT_OVERLAY_SRC := vendor/xiaomi/klimt/proprietary/vendor/overlay

define klimt-vendor-overlay
include $(CLEAR_VARS)
LOCAL_MODULE := $(1)
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := .apk
LOCAL_MODULE_TAGS := optional
LOCAL_PREBUILT_MODULE_FILE := $(KLIMT_OVERLAY_SRC)/$(2)
LOCAL_MODULE_PATH := $(TARGET_OUT_VENDOR)/overlay
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_DEX_PREOPT := false
LOCAL_VENDOR_MODULE := true
include $(BUILD_PREBUILT)
endef

$(eval $(call klimt-vendor-overlay,CellbroadcastUIResOverlay,CellbroadcastUIResOverlay/CellbroadcastUIResOverlay.apk))
$(eval $(call klimt-vendor-overlay,FrameworkResOverlay,FrameworkResOverlay/FrameworkResOverlay.apk))
$(eval $(call klimt-vendor-overlay,FrameworkResOverlayExt,FrameworkResOverlayExt/FrameworkResOverlayExt.apk))
$(eval $(call klimt-vendor-overlay,FrameworkResOverlay_klimt,FrameworkResOverlay_klimt.apk))
$(eval $(call klimt-vendor-overlay,MtkSettingsResOverlay,MtkSettingsResOverlay/MtkSettingsResOverlay.apk))
$(eval $(call klimt-vendor-overlay,MtkTelephonyServiceResOverlay,MtkTelephonyServiceResOverlay/MtkTelephonyServiceResOverlay.apk))
$(eval $(call klimt-vendor-overlay,NewCallDcOverlay,NewCallDcOverlay/NewCallDcOverlay.apk))
$(eval $(call klimt-vendor-overlay,SecureElementResOverlay,SecureElementResOverlay/SecureElementResOverlay.apk))
$(eval $(call klimt-vendor-overlay,SettingsProviderResOverlay,SettingsProviderResOverlay/SettingsProviderResOverlay.apk))
$(eval $(call klimt-vendor-overlay,WifiResMainlineOverlay,WifiResMainlineOverlay/WifiResMainlineOverlay.apk))
$(eval $(call klimt-vendor-overlay,WifiResOverlay,WifiResOverlay/WifiResOverlay.apk))
