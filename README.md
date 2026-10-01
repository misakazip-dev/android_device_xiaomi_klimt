# Device Tree for Xiaomi 15T Pro (klimt)

## Spec Sheet

| Feature          | Specification                                                                                                                   |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| CPU              | Octa-core (1x3.73 GHz Cortex-X925 & 3x3.3 GHz Cortex-X4 & 4x2.4 GHz Cortex-A720)                                                |
| Chipset          | MediaTek Dimensity 9400+ (3 nm)                                                                                                 |
| GPU              | Immortalis-G925 MC12                                                                                                            |
| Memory           | 12 GB LPDDR5X                                                                                                                   |
| Shipped Software | Android 15, HyperOS 2                                                                                                           |
| Storage          | 256 GB, 512 GB, or 1 TB UFS 4.1                                                                                                 |
| Battery          | 5500 mAh                                                                                                                        |
| Dimensions       | 162.7 x 77.9 x 7.96 mm (6.41 x 3.07 x 0.31 in)                                                                                 |
| Display          | 1280 x 2772 pixels, 6.83 inches, 144 Hz AMOLED (~447 ppi density)                                                               |
| Rear Camera      | 50 MP, f/1.62, 23mm (wide), OIS; 50 MP, f/3.0, 115mm (periscope telephoto), OIS; 12 MP, f/2.2, 15mm (ultrawide)                 |
| Front Camera     | 32 MP, f/2.2, 21mm (wide)                                                                                                      |
| Release Date     | 2025, September 24                                                                                                              |

## Device Picture

![Xiaomi 15T Pro](https://i02.appmifile.com/342_operator_sg/23/09/2025/ceb75db860c291fc55faf8fd52d93bb6.png)

## Building

This example targets WitAqua `17.0` / LineageOS `lineage-24.0` and uses the
`github` remote from that ROM manifest.

The kernel and proprietary repositories are not part of the ROM manifest, and
`device/mediatek/sepolicy_vndr` has to exist before `lunch` can evaluate
`BoardConfig.mk`, so sync them with a local manifest, e.g.
`.repo/local_manifests/klimt.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <remote name="misakazip" fetch="https://github.com/misakazip-dev" />
  <remote name="miru10" fetch="https://gitlab.miru10.net/misakazip" />

  <project path="device/xiaomi/klimt" name="android_device_xiaomi_klimt" remote="misakazip" revision="17.0" />
  <project path="kernel/xiaomi/klimt" name="android_kernel_xiaomi_klimt" remote="misakazip" revision="17.0" clone-depth="1" />
  <project path="kernel/xiaomi/klimt-prebuilt" name="android_kernel_xiaomi_klimt-prebuilt" remote="misakazip" revision="17.0" clone-depth="1" />
  <project path="vendor/xiaomi/klimt" name="android_vendor_xiaomi_klimt" remote="miru10" revision="17.0" clone-depth="1" />

  <project path="device/mediatek/sepolicy_vndr" name="LineageOS/android_device_mediatek_sepolicy_vndr" remote="github" revision="lineage-24.0" />
  <project path="hardware/xiaomi" name="LineageOS/android_hardware_xiaomi" remote="github" revision="lineage-24.0" />
</manifest>
```

For an existing source tree, merge these entries into your local manifests by
`path` rather than adding a second entry for a project already present (including
entries in `roomservice.xml`). If an existing `hardware/xiaomi` entry still uses
`lineage-23.2`, update its revision explicitly; roomservice does not change it.

Save the manifest and run `repo sync` from the ROM source root before sourcing
`build/envsetup.sh` and running `lunch`. roomservice sees the projects already
listed in the local manifest and does not add them again from
`lineage.dependencies`.

### Proprietary files

Do not use the published GitLab vendor tree as is. At `18ceea5` it predates the
device tree: it lacks the NXP StrongBox stack and
`fingerprint.goodix_fod.default.so`, and it still ships the HIDL
`vendor.xiaomi.hardware.fingerprintextension@1.0` prebuilts. With
`hardware/xiaomi` in `PRODUCT_SOONG_NAMESPACES`, Soong analysis then stops with
`found in multiple namespaces(vendor/xiaomi/klimt and hardware/xiaomi)`.

Regenerate it from the global `OS3.0.335.0.XOSMIXM` OTA instead (its vendor and odm
identify as `OS3.0.335.0.XOSMI`, which matches `proprietary-files.txt`):

```bash
# Extract the payload and the erofs partitions somewhere outside the tree
prebuilts/extract-tools/linux-x86/bin/ota_extractor --payload payload.bin     --output-dir images --partitions vendor,odm,vendor_dlkm,system,system_ext,product,mi_ext
for p in vendor odm vendor_dlkm system system_ext product mi_ext; do
    fsck.erofs --extract=dump/$p images/$p.img
done
cd device/xiaomi/klimt && ./extract-files.py /path/to/dump
```

The four `MobileFeliCa*` APKs come from the Japanese build
(`klimt_jp OS3.0.302.0.WOSJPXM`) and must be placed in the dump under
`mi_ext/product/app/<name>/` first; every other entry is in the global OTA.
