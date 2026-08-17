#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: WitAqua
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import blob_fixup
from extract_utils.fixups_lib import lib_fixups
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import DEFAULT_PATCHELF_VERSION, patchelf_version_path_map
from extract_utils.utils import run_cmd


def set_soname(soname):
    return blob_fixup().call(
        lambda _ctx, _file, file_path, **_kwargs: run_cmd(
            [patchelf_version_path_map[DEFAULT_PATCHELF_VERSION], '--set-soname', soname, file_path]
        )
    )

lib_fixups = {
    **lib_fixups,
    'libformatter': lambda *_: 'libformatter_vendor',
    'libmnl': lambda *_: 'libmnl_mt6991',
}

namespace_imports = [
    'device/xiaomi/klimt',
]

blob_fixups = {
    (
        'odm/lib64/libHISCppAlgos.so',
        'odm/lib64/libarcsoft_turbo_fusion_raw_portrait_super_night.so',
        'odm/lib64/libhis_motion_tracker.so',
        'odm/lib64/libremosaiclib.so',
        'vendor/lib64/lib3a.ae.pipe.so',
        'vendor/lib64/lib3a.ae.so',
        'vendor/lib64/lib3a.af.core.so',
        'vendor/lib64/lib3a.awb.core.so',
        'vendor/lib64/lib3a.awbsync.so',
        'vendor/lib64/lib3a.flash.so',
        'vendor/lib64/lib3a.flicker.so',
        'vendor/lib64/libDBAccessor_ISP.so',
        'vendor/lib64/libaaa_aaautil.so',
        'vendor/lib64/libaaa_afassist_V2.so',
        'vendor/lib64/libaaa_afassistctrl.so',
        'vendor/lib64/libaaa_feature.so',
        'vendor/lib64/libaaa_toneutil.so',
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
    'odm/lib64/libremosaic_wrapper_odm.so': set_soname('libremosaic_wrapper_odm.so'),
    'vendor/lib64/libcrypto_vendor.so': set_soname('libcrypto_vendor.so'),
    'vendor/lib64/libaudioutils_vendor.so': set_soname('libaudioutils_vendor.so'),
    'vendor/lib64/libjpegdecoder_vendor.so': set_soname('libjpegdecoder_vendor.so'),
    'vendor/lib64/libjpegencoder_vendor.so': set_soname('libjpegencoder_vendor.so'),
    'vendor/lib64/libgui_vendor.so': set_soname('libgui_vendor.so').binary_regex_replace(
        rb'android\.hardware\.graphics\.common-V5-ndk\.so',
        b'android.hardware.graphics.common-V7-ndk.so',
    ),
    'vendor/lib64/libpcap_vendor.so': set_soname('libpcap_vendor.so'),
    'vendor/lib64/libmnl_mt6991.so': set_soname('libmnl_mt6991.so'),
    'vendor/lib64/libprocessgroup_vendor.so': set_soname('libprocessgroup_vendor.so'),
    'odm/lib64/libmiremosaic.so': blob_fixup().replace_needed(
        'libremosaic_wrapper.so', 'libremosaic_wrapper_odm.so'
    ),
    'vendor/lib64/libpkm.so': blob_fixup().replace_needed(
        'libpcap.so', 'libpcap_vendor.so'
    ),
    'vendor/lib64/android.hardware.audio.core-impl-mediatek.so': blob_fixup().replace_needed(
        'libaudioutils.so', 'libaudioutils_vendor.so'
    ),
    'vendor/bin/hw/vendor.xiaomi.hardware.videoservice-service': blob_fixup().replace_needed(
        'libgui.so', 'libgui_vendor.so'
    ),
    (
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.gainmap.so',
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.jpegrAggr.so',
    ): blob_fixup().replace_needed('libultrahdr.so', 'libultrahdr_vendor.so'),
    'vendor/lib64/libultrahdr_vendor.so': set_soname('libultrahdr_vendor.so').replace_needed(
        'libjpegdecoder.so', 'libjpegdecoder_vendor.so'
    ).replace_needed(
        'libjpegencoder.so', 'libjpegencoder_vendor.so'
    ),
    (
        'vendor/bin/aee_aedv64_v2',
        'vendor/bin/aee_dumpstatev_v2',
    ): blob_fixup().replace_needed('libcrypto.so', 'libcrypto_vendor.so'),
    (
        'vendor/lib64/libcameraopt.so',
        'vendor/lib64/libmtkcam_taskmgr.so',
        'vendor/lib64/mt6991/libmtkcam_taskmgr.so',
    ): blob_fixup().replace_needed(
        'libprocessgroup.so', 'libprocessgroup_vendor.so'
    ),
    (
        'odm/lib64/libgoogleid.so',
        'odm/lib64/libmt_mitee.so',
        'vendor/bin/hw/android.hardware.security.keymint-service.strongbox.nxp',
        'vendor/bin/hw/android.hardware.security.keymint@3.0-service.mitee',
        'vendor/lib64/libjc_keymint.nxp.so',
        'vendor/lib64/libjc_keymint_transport.nxp.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.security\.keymint-V[34]-ndk\.so',
        b'android.hardware.security.keymint-V4-ndk.so',
    ),
    (
        'vendor/lib64/hw/android.hardware.audio.effect.aidl-impl-mediatek.so',
        'vendor/lib64/hw/audio.primary.mediatek.so',
        'vendor/lib64/hw/audio.primary.mt6991.so',
        'vendor/lib64/libmisoundfx_mtk_aidl_ext.so',
        'vendor/lib64/libswspatializer_mtk_aidl_ext.so',
        'vendor/lib64/soundfx/libaecsw.so',
        'vendor/lib64/soundfx/libaecsw_mtk.so',
        'vendor/lib64/soundfx/libagc1sw.so',
        'vendor/lib64/soundfx/libagc1sw_mtk.so',
        'vendor/lib64/soundfx/libagc2sw.so',
        'vendor/lib64/soundfx/libagc2sw_mtk.so',
        'vendor/lib64/soundfx/libbassboostsw.so',
        'vendor/lib64/soundfx/libbundleaidl.so',
        'vendor/lib64/soundfx/libdlbvolaidl.so',
        'vendor/lib64/soundfx/libdownmixaidl.so',
        'vendor/lib64/soundfx/libdynamicsprocessingaidl.so',
        'vendor/lib64/soundfx/libenvreverbsw.so',
        'vendor/lib64/soundfx/libequalizersw.so',
        'vendor/lib64/soundfx/libextensioneffect.so',
        'vendor/lib64/soundfx/libhapticgeneratoraidl.so',
        'vendor/lib64/soundfx/libhwdapaidl.so',
        'vendor/lib64/soundfx/libloudnessenhanceraidl.so',
        'vendor/lib64/soundfx/libnssw.so',
        'vendor/lib64/soundfx/libnssw_mtk.so',
        'vendor/lib64/soundfx/libpreprocessingaidl.so',
        'vendor/lib64/soundfx/libpreprocessingaidl_mtk.so',
        'vendor/lib64/soundfx/libpresetreverbsw.so',
        'vendor/lib64/soundfx/libreverbaidl.so',
        'vendor/lib64/soundfx/libspatializermtkaidl.so',
        'vendor/lib64/soundfx/libswdapaidl.so',
        'vendor/lib64/soundfx/libswgamedapaidl.so',
        'vendor/lib64/soundfx/libswspatializeraidl.so',
        'vendor/lib64/soundfx/libvirtualizersw.so',
        'vendor/lib64/soundfx/libvisualizeraidl.so',
        'vendor/lib64/soundfx/libvolumesw.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.effect-V2-ndk\.so',
        b'android.hardware.audio.effect-V4-ndk.so',
    ),
    (
        'odm/bin/test-nusensors',
        'odm/bin/hw/mfp-daemon',
        'odm/bin/hw/vendor.xiaomi.hw.touchfeature-service',
        'odm/bin/hw/vendor.xiaomi.sensor.citsensorservice.aidl',
        'odm/lib64/hw/displayfeature.default.so',
        'odm/lib64/libadaptivehdr.so',
        'odm/lib64/libflatmode.so',
        'odm/lib64/libcolortempmode.so',
        'odm/lib64/libdither.so',
        'odm/lib64/libhistprocess.so',
        'odm/lib64/libmiBrightness.so',
        'odm/lib64/libmiSensorCtrl.so',
        'odm/lib64/libpaperMode.so',
        'odm/lib64/librhytheyecare.so',
        'odm/lib64/libsdr2hdr.so',
        'odm/lib64/libsre.so',
        'odm/lib64/libtruetone.so',
        'odm/lib64/libvideomode.so',
        'vendor/bin/hw/android.hardware.sensors-service.multihal',
        'vendor/lib64/libaalservice.so',
        'vendor/lib64/libpqconfig.so',
        'vendor/lib64/mt6991/libaalservice.so',
        'vendor/lib64/mt6991/libpqconfig.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.sensors-V2-ndk\.so',
        b'android.hardware.sensors-V3-ndk.so',
    ),
    'vendor/bin/mnld': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.sensors-V2-ndk\.so',
        b'android.hardware.sensors-V3-ndk.so',
    ).replace_needed('libmnl.so', 'libmnl_mt6991.so'),
    'system_ext/bin/hw/android.hardware.audio.parameter_parser.service': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.core-V3-ndk\.so',
        b'android.hardware.audio.core-V4-ndk.so',
    ),
    'vendor/lib64/libaudio_aidl_conversion_common_ndk.so': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.common-V3-ndk\.so',
        b'android.hardware.audio.common-V5-ndk.so',
    ),
    (
        'vendor/etc/camera/mt6899/gma_custom.xml',
        'vendor/etc/camera/mt6991/gma_custom.xml',
    ): blob_fixup().binary_regex_replace(
        rb"\A# Don't add another annotation\n# get sensorID from device/mediatek/common/kernel-headers/kd_imgsensor.h, and convert it to Decimal\n",
        b'',
    ).binary_regex_replace(
        rb'\A',
        b'<FeatureSet>\n',
    ).binary_regex_replace(
        rb'\Z',
        b'\n</FeatureSet>\n',
    ),
    'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.soundtrigger3-V2-ndk\.so',
        b'android.hardware.soundtrigger3-V4-ndk.so',
    ),
    (
        'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek',
        'vendor/lib64/android.hardware.audio.core-impl-mediatek.so',
        'vendor/lib64/android.hardware.bluetooth.audio-impl-mediatek.so',
        'vendor/lib64/hw/audio.bluetooth.default.so',
        'vendor/lib64/hw/audio.primary.mediatek.so',
        'vendor/lib64/hw/audio.primary.mt6991.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.1-impl.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.bluetooth.audio@2.2-impl.so',
        'vendor/lib64/libbluetooth_audio_session_aidl.so',
        'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so',
        'vendor/lib64/libpowerhal.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.bluetooth\.audio-V4-ndk\.so',
        b'android.hardware.bluetooth.audio-V6-ndk.so',
    ),
    'vendor/lib64/hw/audio.bluetooth.default.so': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.common-V3-ndk\.so',
        b'android.hardware.audio.common-V5-ndk.so',
    ),
    (
        'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek',
        'vendor/lib64/android.hardware.audio.core-impl-mediatek.so',
        'vendor/lib64/libaudioprimarydevicehalifclient.so',
        'vendor/lib64/soundfx/libspatializermtkaidl.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.core-V2-ndk\.so',
        b'android.hardware.audio.core-V4-ndk.so',
    ),
    'vendor/lib64/libnotifyaudiohal.so': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.core-V2-ndk\.so',
        b'android.hardware.audio.core-V4-ndk.so',
    ).fix_soname(),
    (
        'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek',
        'vendor/lib64/android.hardware.audio.core-impl-mediatek.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.core\.sounddose-V2-ndk\.so',
        b'android.hardware.audio.core.sounddose-V4-ndk.so',
    ),
    'vendor/bin/hw/android.hardware.audio.service-aidl.mediatek': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.soundtrigger3-V2-ndk\.so',
        b'android.hardware.soundtrigger3-V4-ndk.so',
    ),
    (
        'vendor/lib64/libmisoundfx_mtk_aidl_ext.so',
        'vendor/lib64/soundfx/libspatializermtkaidl.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.media\.audio\.common\.types-V3-ndk\.so',
        b'android.media.audio.common.types-V5-ndk.so',
    ),
    (
        'vendor/bin/hw/android.hardware.graphics.allocator-V2-service-mediatek.mt6991',
        'vendor/bin/hw/mt6991/android.hardware.graphics.allocator-V2-service-mediatek.mt6991',
        'vendor/lib64/egl/libGLES_mali.so',
        'vendor/lib64/egl/mt6991/libGLES_mali.so',
        'vendor/lib64/hw/mapper.mediatek.so',
        'vendor/lib64/hw/mt6991/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/mt6991/mapper.mediatek.so',
        'vendor/lib64/libaimemc.so',
        'vendor/lib64/libcodec2_fsr.so',
        'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
        'vendor/lib64/libcodec2_vpp_AISR_plugin.so',
        'vendor/lib64/libgpud.so',
        'vendor/lib64/libmtkcam_grallocutils.so',
        'vendor/lib64/libmtkcam_grallocutils_aidlv2helper.so',
        'vendor/lib64/mt6991/libmtkcam_grallocutils.so',
        'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.graphics\.common-V5-ndk\.so',
        b'android.hardware.graphics.common-V7-ndk.so',
    ),
    (
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-V1-ndk.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-client.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-service.so',
    ): blob_fixup().binary_regex_replace(
        rb'android\.hardware\.camera\.device-V1-ndk\.so',
        b'android.hardware.camera.device-V2-ndk.so',
    ),
    'vendor/lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so': blob_fixup().binary_regex_replace(
        rb'android\.hardware\.audio\.common-V3-ndk\.so',
        b'android.hardware.audio.common-V5-ndk.so',
    ),
}

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
