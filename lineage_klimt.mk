#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

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
    BuildDesc="missi-user 16 BP2A.250605.031.A3 16OS3.1.260420.011757416.MTPEGL.S release-keys" \
    BuildFingerprint=Xiaomi/klimt_jp/klimt:16/BP2A.250605.031.A3/OS3.0.301.0.WOSJPXM:user/release-keys
