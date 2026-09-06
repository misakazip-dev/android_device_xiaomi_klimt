#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# WitAqua
WITAQUA_MAINTAINER := Misaka (@misakazip)
PROCESSOR_INFO := MediaTek Dimensity 9400+
CAMERA_REAR_INFO := 50,50,12
CAMERA_FRONT_INFO := 32

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from klimt device
$(call inherit-product, device/xiaomi/klimt/device.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_DEVICE := klimt
PRODUCT_NAME := lineage_klimt
PRODUCT_BRAND := Xiaomi
PRODUCT_MODEL := Xiaomi 15T Pro
PRODUCT_MANUFACTURER := Xiaomi

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="klimt_global-user 15 AP3A.240905.015.A2 OS3.0.335.0.XOSMIXM release-keys" \
    BuildFingerprint=Xiaomi/klimt_global/klimt:15/AP3A.240905.015.A2/OS3.0.335.0.XOSMI:user/release-keys
