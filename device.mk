#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Enable updating of APEXes
$(call inherit-product, $(SRC_TARGET_DIR)/product/updatable_apex.mk)

# A/B
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/vabc_features.mk)

PRODUCT_VENDOR_PROPERTIES += \
    ro.virtual_ab.compression.threads=true

PRODUCT_VIRTUAL_AB_COMPRESSION_METHOD := lz4
PRODUCT_VIRTUAL_AB_COMPRESSION_FACTOR := 65536

PRODUCT_PACKAGES += \
    snapuserd_ramdisk \
    snapuserd.recovery

# API levels
PRODUCT_SHIPPING_API_LEVEL := 35

# Audio
# The stock MediaTek V1 methods, parcel order and virtual slots match this API.
PRODUCT_PACKAGES += \
    vendor.mediatek.hardware.audio-V1-ndk.vendor

PRODUCT_PACKAGES += \
    android.hardware.bluetooth.audio-impl \
    android.hardware.bluetooth.audio@2.0-impl \
    android.hardware.bluetooth.audio@2.1-impl \
    audio.bluetooth.default \
    libbassboostsw \
    libbluetooth_audio_session \
    libbundleaidl \
    libdownmixaidl \
    libdynamicsprocessingaidl \
    libequalizersw \
    libextensioneffect \
    libhapticgeneratoraidl \
    libloudnessenhanceraidl \
    libpresetreverbsw \
    libreverbaidl \
    libvirtualizersw \
    libvisualizeraidl \
    libvolumesw

# Dolby Atmos
PRODUCT_PACKAGES += \
    DolbyAtmos

# Boot control
PRODUCT_PACKAGES += \
    android.hardware.boot-service.default_recovery

PRODUCT_PACKAGES += \
    update_engine \
    update_engine_sideload \
    update_verifier

# Xiaomi camera application and its public JNI libraries.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/permissions/default-permissions-miuicamera.xml:$(TARGET_COPY_OUT_PRODUCT)/etc/default-permissions/default-permissions-miuicamera.xml \
    $(LOCAL_PATH)/configs/permissions/privapp-permissions-miuicamera.xml:$(TARGET_COPY_OUT_PRODUCT)/etc/permissions/privapp-permissions-miuicamera.xml \
    $(LOCAL_PATH)/configs/sysconfig/miuicamera-hiddenapi-package-allowlist.xml:$(TARGET_COPY_OUT_PRODUCT)/etc/sysconfig/miuicamera-hiddenapi-package-allowlist.xml \
    $(LOCAL_PATH)/configs/public.libraries-xiaomi.txt:$(TARGET_COPY_OUT_SYSTEM)/etc/public.libraries-xiaomi.txt

# Common MediaTek diagnostics and SoC information
PRODUCT_PACKAGES += \
    chipinfo \
    libaedv \
    libladder

# Display memory accounting
PRODUCT_PACKAGES += \
    android.hardware.memtrack-service.mediatek

# DRM
PRODUCT_PACKAGES += \
    android.hardware.drm-service.clearkey

PRODUCT_VENDOR_LINKER_CONFIG_FRAGMENTS += \
    $(LOCAL_PATH)/configs/linker/linker.config.json

# eUICC (Japanese hardware SKU only; selected by libinit)
PRODUCT_PACKAGES += \
    XiaomiEuicc \
    EuiccPolicyResKlimt \
    FrameworksResKlimtEsim

# MediaTek slot switcher and its vendor modem bridge.
PRODUCT_PACKAGES += \
    EsimSwitcher \
    init.esim.rc \
    init.esim.sh

# fastbootd
PRODUCT_PACKAGES += \
    android.hardware.fastboot-service.example_recovery \
    fastbootd

# Health
PRODUCT_PACKAGES += \
    android.hardware.health-service.example \
    android.hardware.health-service.example_recovery

# MediaTek framework compatibility
PRODUCT_PACKAGES += \
    mediatek-common

PRODUCT_BOOT_JARS += \
    system_ext:mediatek-common

# IMS
PRODUCT_PACKAGES += \
    KlimtProtectedBroadcasts

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/permissions/privapp-permissions-com.mediatek.ims.xml:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/permissions/privapp-permissions-com.mediatek.ims.xml

# Fingerprint
PRODUCT_PACKAGES += \
    android.hardware.biometrics.fingerprint-service.xiaomi \
    libudfpshandler

# IR
PRODUCT_PACKAGES += \
    android.hardware.ir-service.example

# Kernel
PRODUCT_ENABLE_UFFD_GC := true

# Keymint
PRODUCT_PACKAGES += \
    libkeymaster4support.vendor \
    libkeymint_remote_prov_support.vendor \
    libkeymint_support.vendor

# MediaTek power clients and versioned interfaces
PRODUCT_PACKAGES += \
    libmtkperf_client_vendor \
    libperfctl_vendor \
    libpowerhalwrap_vendor \
    vendor.mediatek.hardware.mtkpower@1.0 \
    vendor.mediatek.hardware.mtkpower@1.1 \
    vendor.mediatek.hardware.mtkpower@1.2

# NFC
PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.nfc.ese.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.nfc.ese.xml \
    frameworks/native/data/etc/android.hardware.nfc.hce.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.nfc.hce.xml \
    frameworks/native/data/etc/android.hardware.nfc.hcef.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.nfc.hcef.xml \
    frameworks/native/data/etc/android.hardware.nfc.uicc.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.nfc.uicc.xml \
    frameworks/native/data/etc/android.hardware.nfc.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.nfc.xml \
    frameworks/native/data/etc/android.hardware.se.omapi.ese.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.se.omapi.ese.xml \
    frameworks/native/data/etc/android.hardware.se.omapi.uicc.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.se.omapi.uicc.xml \
    frameworks/native/data/etc/com.android.nfc_extras.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/com.android.nfc_extras.xml \
    frameworks/native/data/etc/com.nxp.mifare.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/com.nxp.mifare.xml

# Overlays
PRODUCT_ENFORCE_RRO_TARGETS := *

DEVICE_PACKAGE_OVERLAYS += \
    $(LOCAL_PATH)/overlay

# Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# Permissions
PRODUCT_PACKAGES += \
    android.hardware.hardware_keystore.xml

# Product characteristics
PRODUCT_CHARACTERISTICS := nosdcard

# Rootdir
PRODUCT_COPY_FILES += \
    device/xiaomi/klimt/rootdir/etc/fstab.mt6991:$(TARGET_COPY_OUT_VENDOR_RAMDISK)/first_stage_ramdisk/fstab.mt6991 \
    device/xiaomi/klimt/rootdir/etc/fstab.mt6991:$(TARGET_COPY_OUT_RECOVERY)/root/first_stage_ramdisk/fstab.mt6991 \
    device/xiaomi/klimt/rootdir/etc/init.recovery.mt6991.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.mt6991.rc \
    device/xiaomi/klimt/rootdir/etc/ueventd.odm.rc:$(TARGET_COPY_OUT_ODM)/etc/ueventd.rc

PRODUCT_PACKAGES += \
    init.felica.sh \
    init.insmod.sh \
    init.pstore_blk.sh \
    mdota_symlink

PRODUCT_PACKAGES += \
    fstab.mt6991 \
    factory_init.connectivity.common.rc \
    factory_init.connectivity.rc \
    factory_init.project.rc \
    factory_init.rc \
    init.batterysecret.rc \
    init.cgroup.rc \
    init.connectivity.common.rc \
    init.connectivity.rc \
    init.mi_thermald.rc \
    init.modem.rc \
    init.mt6991.rc \
    init.mt6991.usb.rc \
    init.mtkgki.rc \
    init.project.rc \
    init.pstore.rc \
    init.sensor_2_0.rc \
    init_conninfra.rc \
    meta_init.connectivity.common.rc \
    meta_init.connectivity.rc \
    meta_init.modem.rc \
    meta_init.project.rc \
    meta_init.rc \
    meta_init.vendor.rc \
    multi_init.rc

# Sensors
PRODUCT_PACKAGES += \
    android.hardware.sensors-service.multihal

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH) \
    hardware/google/interfaces \
    hardware/google/pixel/pixelstats \
    hardware/mediatek \
    hardware/mediatek/libmtkperf_client \
    hardware/xiaomi

PRODUCT_SOURCE_ROOT_DIRS += \
    -vendor/qcom/opensource/interfaces/qacs

# Thermal HAL reporting; vendor thermal engines retain cooling control.
PRODUCT_PACKAGES += \
    android.hardware.thermal-service.mediatek

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/thermal_info_config.json:$(TARGET_COPY_OUT_VENDOR)/etc/thermal_info_config.json

# Vendor ABI compatibility
PRODUCT_PACKAGES += \
    libprocessgroup \
    libprocessgroup_shim \
    libtinyxml2-v34

# Vendor service manager
PRODUCT_PACKAGES += \
    vndservicemanager

# Wi-Fi
PRODUCT_PACKAGES += \
    android.hardware.wifi-service-lazy \
    wlan_assistant \
    wpa_cli \
    wpa_supplicant

# The Android 15 blob predates the two 11az v4 function pointers.
# Keep the init configuration paired with the stock USB gadget HAL.
$(call soong_config_set_bool,mediatek_gadget,use_custom_usb_gadget_rc,true)

$(call soong_config_set_bool,mediatek_wifi_hal,use_pre_baklava_qpr0_struct,true)

PRODUCT_PACKAGES += \
    libwifi-hal-wrapper

PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.audio.low_latency.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.audio.low_latency.xml \
    frameworks/native/data/etc/android.hardware.biometrics.face.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.biometrics.face.xml \
    frameworks/native/data/etc/android.hardware.bluetooth.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.bluetooth.xml \
    frameworks/native/data/etc/android.hardware.bluetooth_le.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.bluetooth_le.xml \
    frameworks/native/data/etc/android.hardware.camera.concurrent.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.concurrent.xml \
    frameworks/native/data/etc/android.hardware.camera.flash-autofocus.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.flash-autofocus.xml \
    frameworks/native/data/etc/android.hardware.camera.front.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.front.xml \
    frameworks/native/data/etc/android.hardware.camera.full.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.full.xml \
    frameworks/native/data/etc/android.hardware.camera.raw.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.raw.xml \
    frameworks/native/data/etc/android.hardware.consumerir.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.consumerir.xml \
    frameworks/native/data/etc/android.hardware.faketouch.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.faketouch.xml \
    frameworks/native/data/etc/android.hardware.fingerprint.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.fingerprint.xml \
    frameworks/native/data/etc/android.hardware.keystore.app_attest_key.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.keystore.app_attest_key.xml \
    frameworks/native/data/etc/android.hardware.location.gps.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.location.gps.xml \
    frameworks/native/data/etc/android.hardware.opengles.aep.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.opengles.aep.xml \
    frameworks/native/data/etc/android.hardware.sensor.accelerometer.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.accelerometer.xml \
    frameworks/native/data/etc/android.hardware.sensor.compass.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.compass.xml \
    frameworks/native/data/etc/android.hardware.sensor.dynamic.head_tracker.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.dynamic.head_tracker.xml \
    frameworks/native/data/etc/android.hardware.sensor.gyroscope.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.gyroscope.xml \
    frameworks/native/data/etc/android.hardware.sensor.light.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.light.xml \
    frameworks/native/data/etc/android.hardware.sensor.proximity.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.proximity.xml \
    frameworks/native/data/etc/android.hardware.sensor.stepcounter.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.stepcounter.xml \
    frameworks/native/data/etc/android.hardware.sensor.stepdetector.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.stepdetector.xml \
    frameworks/native/data/etc/android.hardware.telephony.euicc.mep.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/sku_klimt_jp/android.hardware.telephony.euicc.mep.xml \
    frameworks/native/data/etc/android.hardware.telephony.euicc.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/sku_klimt_jp/android.hardware.telephony.euicc.xml \
    frameworks/native/data/etc/android.hardware.telephony.gsm.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.gsm.xml \
    frameworks/native/data/etc/android.hardware.telephony.ims.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.ims.xml \
    frameworks/native/data/etc/android.hardware.telephony.satellite.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.satellite.xml \
    frameworks/native/data/etc/android.hardware.touchscreen.multitouch.jazzhand.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.touchscreen.multitouch.jazzhand.xml \
    frameworks/native/data/etc/android.hardware.usb.accessory.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.usb.accessory.xml \
    frameworks/native/data/etc/android.hardware.usb.host.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.usb.host.xml \
    frameworks/native/data/etc/android.hardware.vulkan.compute-0.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.compute-0.xml \
    frameworks/native/data/etc/android.hardware.vulkan.level-1.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.level-1.xml \
    frameworks/native/data/etc/android.hardware.vulkan.version-1_3.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.version-1_3.xml \
    frameworks/native/data/etc/android.hardware.wifi.direct.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.direct.xml \
    frameworks/native/data/etc/android.hardware.wifi.passpoint.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.passpoint.xml \
    frameworks/native/data/etc/android.hardware.wifi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.xml \
    frameworks/native/data/etc/android.software.device_id_attestation.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.device_id_attestation.xml \
    frameworks/native/data/etc/android.software.ipsec_tunnels.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.ipsec_tunnels.xml \
    frameworks/native/data/etc/android.software.midi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.midi.xml \
    frameworks/native/data/etc/android.software.opengles.deqp.level-2024-03-01.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.opengles.deqp.level.xml \
    frameworks/native/data/etc/android.software.verified_boot.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.verified_boot.xml \
    frameworks/native/data/etc/android.software.vulkan.deqp.level-2024-03-01.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.vulkan.deqp.level.xml \
    frameworks/native/data/etc/handheld_core_hardware.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/handheld_core_hardware.xml

# Inherit the proprietary files
$(call inherit-product, vendor/xiaomi/klimt/klimt-vendor.mk)
