#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
import re
from zipfile import ZipFile

from extract_utils.fixups_blob import blob_fixup
from extract_utils.fixups_lib import lib_fixups
from extract_utils.tools import apktool_path, java_path
from extract_utils.utils import run_cmd
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/klimt',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]


def camera_resource(name):
    return name == 'resources.arsc' or name.startswith(('res/', 'assets/obfu_res/'))


def unpack_miuicamera(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    assert tmp_dir is not None
    run_cmd([
        java_path, '-jar', apktool_path, 'd',
        file_path, '-o', tmp_dir, '-f',
    ])
    # Save resources outside the decoded res/ directory for restoration.
    with ZipFile(file_path) as source, ZipFile(
        os.path.join(tmp_dir, 'original', 'camera-resources.zip'), 'w'
    ) as saved:
        for entry in source.infolist():
            if camera_resource(entry.filename):
                saved.writestr(entry, source.read(entry.filename))


def pack_miuicamera(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    assert tmp_dir is not None
    run_cmd([
        java_path, '-jar', apktool_path, 'b', tmp_dir, '-o', file_path,
    ])
    # Keep the rebuilt binary manifest and dex, but restore ResGuard paths.
    # The decoded public.xml preserves the original resource IDs.
    rebuilt_path = file_path + '.rebuilt'
    with ZipFile(file_path) as rebuilt, ZipFile(
        os.path.join(tmp_dir, 'original', 'camera-resources.zip')
    ) as saved, ZipFile(rebuilt_path, 'w') as output:
        assert 'AndroidManifest.xml' in rebuilt.namelist()
        for entry in rebuilt.infolist():
            if not camera_resource(entry.filename):
                output.writestr(entry, rebuilt.read(entry.filename))
        for entry in saved.infolist():
            # Drop stock ZIP extra fields unsupported by stripzip.
            entry.extra = b''
            output.writestr(entry, saved.read(entry.filename))
    os.replace(rebuilt_path, file_path)


def aidl_bump(interface: str, from_version: int, to_version: int):
    return blob_fixup().binary_regex_replace(
        re.escape(f'{interface}-V{from_version}-ndk.so'.encode()),
        f'{interface}-V{to_version}-ndk.so'.encode(),
    )


lib_fixups = {
    **lib_fixups,
    'libformatter': lambda *_: 'libformatter_vendor',
    'libmnl': lambda *_: 'libmnl_mt6991',
    'libsink': lambda *_: 'libsink_system_ext',
    # Camera JNI dependencies use system modules, preserving their ELF names.
    (
        'libmtkisp_metadata_sys',
        'vendor.mediatek.hardware.camera.isphal-V1-ndk',
        'vendor.mediatek.hardware.camera.isphal@1.0',
    ): lambda lib, partition: f'{lib}_miuicamera' if partition == 'system' else None,
}

# Blobs built against the A15 audio AIDL. The platform ships newer versions
# whose parcelable layouts differ, so the A15 interface libraries and the
# matching conversion library are installed under a _vendor suffix and the
# whole stack is pointed at them.
a15_audio_stack = (
    'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek',
    'vendor/lib64/android.hardware.audio.common_v3_vendor.so',
    'vendor/lib64/android.hardware.audio.core-impl-mediatek.so',
    'vendor/lib64/android.hardware.audio.core.sounddose_v2_vendor.so',
    'vendor/lib64/android.hardware.audio.core_v2_vendor.so',
    'vendor/lib64/android.hardware.audio.effect_v2_vendor.so',
    'vendor/lib64/android.hardware.bluetooth.audio-impl-mediatek.so',
    'vendor/lib64/android.hardware.bluetooth.audio_v4_vendor.so',
    'vendor/lib64/hw/android.hardware.audio.effect.aidl-impl-mediatek.so',
    'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so',
    'vendor/lib64/hw/audio.primary.mediatek.so',
    'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.1-impl.so',
    'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.2-impl.so',
    'vendor/lib64/libaudio_aidl_conversion_common_ndk_vendor.so',
    'vendor/lib64/libaudioprimarydevicehalifclient.so',
    'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so',
    'vendor/lib64/libmisoundfx_mtk_aidl_ext.so',
    'vendor/lib64/libnotifyaudiohal.so',
    'vendor/lib64/libpowerhal.so',
    'vendor/lib64/libswspatializer_mtk_aidl_ext.so',
    'vendor/lib64/soundfx/libaecsw_mtk.so',
    'vendor/lib64/soundfx/libagc1sw_mtk.so',
    'vendor/lib64/soundfx/libagc2sw_mtk.so',
    'vendor/lib64/soundfx/libdlbvolaidl.so',
    'vendor/lib64/soundfx/libenvreverbsw.so',
    'vendor/lib64/soundfx/libhwdapaidl.so',
    'vendor/lib64/soundfx/libnssw_mtk.so',
    'vendor/lib64/soundfx/libpreprocessingaidl_mtk.so',
    'vendor/lib64/soundfx/libspatializermtkaidl.so',
    'vendor/lib64/soundfx/libswdapaidl.so',
    'vendor/lib64/soundfx/libswgamedapaidl.so',
    'vendor/lib64/soundfx/libswspatializeraidl.so',
    'vendor/lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so',
)

blob_fixups = {
    'product/priv-app/MiuiCamera/MiuiCamera.apk': blob_fixup()
    .call(unpack_miuicamera)
    .patch_dir('patches/MiuiCamera')
    .call(pack_miuicamera)
    .stripzip(),
    # Libraries renamed in proprietary-files.txt, plus libnotifyaudiohal whose
    # stock SONAME is libnotifyaudiohal@aidl-2.0.so.
    (
        'odm/lib64/libremosaic_wrapper_odm.so',
        'vendor/lib64/android.hardware.audio.common_v3_vendor.so',
        'vendor/lib64/android.hardware.audio.core.sounddose_v2_vendor.so',
        'vendor/lib64/android.hardware.audio.core_v2_vendor.so',
        'vendor/lib64/android.hardware.audio.effect_v2_vendor.so',
        'vendor/lib64/android.hardware.bluetooth.audio_v4_vendor.so',
        'vendor/lib64/android.media.audio.common.types_v3_vendor.so',
        'vendor/lib64/android.media.audio.common.types_v5_vendor.so',
        'vendor/lib64/libaudio_aidl_conversion_common_ndk_vendor.so',
        'vendor/lib64/libaudioutils_vendor.so',
        'vendor/lib64/libcrypto_vendor.so',
        'vendor/lib64/libgui_vendor.so',
        'vendor/lib64/libjpegdecoder_vendor.so',
        'vendor/lib64/libjpegencoder_vendor.so',
        'vendor/lib64/libmnl_mt6991.so',
        'vendor/lib64/libnotifyaudiohal.so',
        'vendor/lib64/libpcap_vendor.so',
        'vendor/lib64/libperfctl_stock.so',
        'vendor/lib64/libultrahdr_vendor.so',
        'vendor/lib64/libwifi-hal-mtk.so',
    ): blob_fixup().fix_soname(),
    a15_audio_stack: blob_fixup()
    .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common_v3_vendor.so')
    .replace_needed('android.hardware.audio.core-V2-ndk.so', 'android.hardware.audio.core_v2_vendor.so')
    .replace_needed('android.hardware.audio.core.sounddose-V2-ndk.so', 'android.hardware.audio.core.sounddose_v2_vendor.so')
    .replace_needed('android.hardware.audio.effect-V2-ndk.so', 'android.hardware.audio.effect_v2_vendor.so')
    .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio_v4_vendor.so')
    .replace_needed('android.media.audio.common.types-V3-ndk.so', 'android.media.audio.common.types_v3_vendor.so')
    .replace_needed('android.media.audio.common.types-V5-ndk.so', 'android.media.audio.common.types_v5_vendor.so')
    .replace_needed('libaudio_aidl_conversion_common_ndk.so', 'libaudio_aidl_conversion_common_ndk_vendor.so'),
    # FPSGO expects xgfGetCmd to return a 40-byte struct through the AArch64
    # indirect-result register. The shared perfctl stub has a different ABI.
    'vendor/bin/fpsgo': blob_fixup().binary_regex_replace(
        re.escape(b'libperfctl_vendor.so\x00'), b'libperfctl_stock.so\x00\x00'
    ),
    # VNDK v34 preserves the XMLDocument/XMLPrinter layout used by these blobs.
    # The platform's newer tinyxml2 does not fit their inlined allocations.
    (
        'odm/lib64/hw/displayfeature.default.so',
        'odm/lib64/libmiXmlParser.so',
        'vendor/bin/hw/vendor.xiaomi.hardware.miperf2-service',
        'vendor/lib64/hw/android.hardware.audio.effect.aidl-impl-mediatek.so',
        'vendor/lib64/hw/audio.primary.mediatek.so',
        'vendor/lib64/hw/hwcomposer.mtk_common.so',
        'vendor/lib64/hw/mt6991/vendor.mediatek.hardware.pq_aidl-impl.so',
        'vendor/lib64/libHardwareBacklightcore.so',
        'vendor/lib64/lib_power_applist.so',
        'vendor/lib64/libaudiocloudctrl.so',
        'vendor/lib64/libmicamera_aidl_provider.so',
        'vendor/lib64/libmicamera_hal_core.so',
        'vendor/lib64/libpowerhal.so',
        'vendor/lib64/libpqxmlflagparser.so',
        'vendor/lib64/libpqxmlparser.so',
        'vendor/lib64/librt_extamp_intf.so',
        'vendor/lib64/libsilkybrightnesscore.so',
        'vendor/lib64/libxlog.so',
        'vendor/lib64/mt6991/lib3a.custom.ae.flow.so',
        'vendor/lib64/mt6991/libmmlpqImpl.so',
    ): blob_fixup()
    .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
    .replace_needed('libtinyxml2_vendor.so', 'libtinyxml2-v34.so'),
    # Other platform libraries the A15 blobs need their own copy of.
    'vendor/lib64/android.hardware.audio.core-impl-mediatek.so': blob_fixup()
    .replace_needed('libaudioutils.so', 'libaudioutils_vendor.so'),
    'vendor/bin/hw/vendor.xiaomi.hardware.videoservice-service': blob_fixup()
    .replace_needed('libgui.so', 'libgui_vendor.so'),
    'vendor/lib64/libpkm.so': blob_fixup()
    .replace_needed('libpcap.so', 'libpcap_vendor.so'),
    # The shim restores the old C SetTaskProfiles entry point and delegates
    # to the platform implementation; keep libprocessgroup for get_sched_policy.
    (
        'vendor/lib64/libcameraopt.so',
        'vendor/lib64/mt6991/libmtkcam_taskmgr.so',
    ): blob_fixup()
    .add_needed('libprocessgroup_shim.so'),
    (
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.gainmap.so',
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.jpegrAggr.so',
    ): blob_fixup().replace_needed('libultrahdr.so', 'libultrahdr_vendor.so'),
    'vendor/lib64/libultrahdr_vendor.so': blob_fixup()
    .replace_needed('libjpegdecoder.so', 'libjpegdecoder_vendor.so')
    .replace_needed('libjpegencoder.so', 'libjpegencoder_vendor.so'),
    # Renamed to avoid the platform modules of the same name.
    'vendor/bin/mnld': blob_fixup()
    .replace_needed('libmnl.so', 'libmnl_mt6991.so'),
    'odm/lib64/libmiremosaic.so': blob_fixup()
    .replace_needed('libremosaic_wrapper.so', 'libremosaic_wrapper_odm.so'),
    # Camera 3A blobs resolve libc++ symbols without listing the library.
    (
        'odm/lib64/libHISCppAlgos.so',
        'odm/lib64/libarcsoft_turbo_fusion_raw_portrait_super_night.so',
        'odm/lib64/libhis_motion_tracker.so',
        'odm/lib64/libremosaiclib.so',
        'vendor/lib64/lib3a.ae.pipe.so',
        'vendor/lib64/libaaa_aaautil.so',
        'vendor/lib64/libaaa_afassist_V2.so',
        'vendor/lib64/libaaa_afassistctrl.so',
        'vendor/lib64/libfeaturepolicy.so',
        'vendor/lib64/mt6991/lib3a.ae.so',
        'vendor/lib64/mt6991/lib3a.af.core.so',
        'vendor/lib64/mt6991/lib3a.awb.core.so',
        'vendor/lib64/mt6991/lib3a.awbsync.so',
        'vendor/lib64/mt6991/lib3a.flash.so',
        'vendor/lib64/mt6991/lib3a.flicker.so',
        'vendor/lib64/mt6991/libDBAccessor_ISP.so',
        'vendor/lib64/mt6991/libaaa_feature.so',
        'vendor/lib64/mt6991/libaaa_toneutil.so',
    ): blob_fixup().add_needed('libc++_shared.so'),
    (
        'odm/bin/hw/vendor.xiaomi.hw.touchfeature-service',
        'odm/bin/test-nusensors',
        'odm/lib64/hw/displayfeature.default.so',
        'odm/lib64/libadaptivehdr.so',
        'odm/lib64/libcolortempmode.so',
        'odm/lib64/libdither.so',
        'odm/lib64/libflatmode.so',
        'odm/lib64/libhistprocess.so',
        'odm/lib64/libmiBrightness.so',
        'odm/lib64/libmiSensorCtrl.so',
        'odm/lib64/libpaperMode.so',
        'odm/lib64/librhytheyecare.so',
        'odm/lib64/libsdr2hdr.so',
        'odm/lib64/libsre.so',
        'odm/lib64/libtruetone.so',
        'odm/lib64/libvideomode.so',
        'vendor/bin/mnld',
        'vendor/lib64/mt6991/libaalservice.so',
        'vendor/lib64/mt6991/libpqconfig.so',
    ): aidl_bump('android.hardware.sensors', 2, 3),
    (
        'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek',
        'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so',
    ): aidl_bump('android.hardware.soundtrigger3', 2, 4),
    (
        'vendor/bin/hw/mt6991/android.hardware.graphics.allocator-V2-service-mediatek.mt6991',
        'vendor/lib64/egl/mt6991/libGLES_mali.so',
        'vendor/lib64/hw/mt6991/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/mt6991/mapper.mediatek.so',
        'vendor/lib64/libaimemc.so',
        'vendor/lib64/libcodec2_fsr.so',
        'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
        'vendor/lib64/libcodec2_vpp_AISR_plugin.so',
        'vendor/lib64/libgpud.so',
        'vendor/lib64/libgui_vendor.so',
        'vendor/lib64/libmtkcam_grallocutils_aidlv2helper.so',
        'vendor/lib64/mt6991/libmtkcam_grallocutils.so',
        'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
    ): aidl_bump('android.hardware.graphics.common', 5, 7),
    (
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-V1-ndk.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-client.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-service.so',
    ): aidl_bump('android.hardware.camera.device', 1, 2),
    # Keep the stock device-node/data-directory setup, with a single HAL owner.
    'odm/etc/init/init.mfp-daemon.aidl.rc': blob_fixup()
    .regex_replace(r'\Aservice mfp-daemon[^\n]*\n(?:[ \t]+[^\n]*\n|\n)*', '')
    .regex_replace(r'\b(stop|start) mfp-daemon\b', r'\1 vendor.fingerprint-default'),
    # The stock StrongBox policy grants WAKE_ALARM, but not SYS_ADMIN/SYS_NICE.
    'vendor/etc/init/android.hardware.security.keymint-service.strongbox.nxp.rc': blob_fixup()
    .regex_replace('capabilities SYS_ADMIN SYS_NICE WAKE_ALARM', 'capabilities WAKE_ALARM'),
    # libhardware looks for <class>.<inst>.default.so; the stock name matches no variant.
    'odm/lib64/hw/fingerprint.goodix_fod.default.so': blob_fixup().fix_soname(),
    # The config references env_reverb but never declares the library, so
    # EffectFactory builds the identifier from a failed lookup.
    'vendor/etc/audio_effects_config.xml': blob_fixup()
    .regex_replace(
        r'(\s*)<library name="preset_reverbsw" path="libpresetreverbsw.so"/>',
        r'\1<library name="preset_reverbsw" path="libpresetreverbsw.so"/>'
        r'\1<library name="env_reverbsw" path="libenvreverbsw.so"/>',
    )
    # The A15 blobs build Processing with the V2 layout but link against the V4
    # ndk library, so teardown follows a wild pointer. Drop the processing
    # definitions to make queryProcessing return empty.
    .regex_replace(r'(?s)\s*<postprocess>.*?</postprocess>', '')
    .regex_replace(r'(?s)\s*<preprocess>.*?</preprocess>', ''),
    # AUDIO_FORMAT_MIHC is Xiaomi-only and missing from the platform enum, so
    # AudioPolicyConfigXmlConverter aborts with BAD_VALUE.
    (
        'vendor/etc/audio_policy_configuration_a2dp_offload_enable_cg_enable.xml',
        'vendor/etc/bluetooth_offload_audio_policy_configuration.xml',
    ): blob_fixup().regex_replace(' AUDIO_FORMAT_MIHC', ''),
    # The stock files are bare property lists without the enclosing element.
    (
        'vendor/etc/camera/mt6899/gma_custom.xml',
        'vendor/etc/camera/mt6991/gma_custom.xml',
    ): blob_fixup()
    .regex_replace(r'\A(?:#[^\n]*\n)*', '<FeatureSet>\n')
    .regex_replace(r'\Z', '\n</FeatureSet>\n'),
}

# Keep the NXP service's C++ Keymaster/CBOR dependencies from the same ROM.
# AIDL version bumps alone do not preserve the ABI of these C++ classes.
strongbox_libraries = (
    'lib_android_keymaster_keymint_utils',
    'libcppbor',
    'libcppcose_rkp',
    'libkeymaster_messages',
    'libkeymaster_portable',
    'libsoft_attestation_cert',
)
strongbox_private_paths = tuple(
    f'vendor/lib64/{name}_strongbox.so' for name in strongbox_libraries
)
strongbox_fixup = blob_fixup()
for name in strongbox_libraries:
    strongbox_fixup.replace_needed(f'{name}.so', f'{name}_strongbox.so')
strongbox_fixup.replace_needed('libcrypto.so', 'libcrypto_vendor.so')

# Keep the stock KeyMint V3 dependency: replacing it with V4 changes the
# generated Bn service ABI. The platform still builds the frozen V3 interface.
for file in (
    'vendor/bin/hw/android.hardware.security.keymint-service.strongbox.nxp',
    'vendor/lib64/libjc_keymint.nxp.so',
    'vendor/lib64/libjc_keymint_transport.nxp.so',
    *strongbox_private_paths,
):
    fixup = blob_fixup()
    fixup.merge(strongbox_fixup)
    if file in strongbox_private_paths:
        fixup.fix_soname()
    blob_fixups[file] = fixup

module = ExtractUtilsModule(
    'klimt',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
