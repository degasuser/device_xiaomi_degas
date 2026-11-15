# Xiaomi 14T (degas) — PixelOS 17

Device tree for **Xiaomi 14T**, targeting [PixelOS seventeen / Android 17](https://github.com/PixelOS-AOSP/android_manifest/tree/seventeen). The PixelOS adaptation is maintained in the [`pixelos-17` branch](https://github.com/mt6897-degas/android_device_xiaomi_degas/tree/pixelos-17).

The original **degas device tree was created by [Mikhail Mlhcnn (Advnirr)](https://github.com/Advnirr)** and published by [Degas Developers](https://github.com/degas-developers/android_device_xiaomi_degas). This adaptation is based on their `lineage-23.2` tree at [`e7de73fe295ff07eb08927c9c8c61b536a2cd378`](https://github.com/degas-developers/android_device_xiaomi_degas/commit/e7de73fe295ff07eb08927c9c8c61b536a2cd378).

| Item | Specification |
| --- | --- |
| Device | Xiaomi 14T, codename `degas`, model `2406APNFAG` |
| SoC | MediaTek Dimensity 8300-Ultra / MT6897 |
| GPU | Mali-G615 MC6 |
| Display | 6.67-inch AMOLED, 1220 × 2712, up to 144 Hz |
| ROM target | PixelOS 17, `custom_degas`, `userdebug` |
| Stock base | HyperOS **OS3.0.306.0.WNEEUXM**, EEA, Android 16 |
| Vendor API / VINTF level | 34 / 8 |
| Super partition | 9,663,676,416 bytes |

## Status

A full Android 17 build completed on November 13, 2026. Subsequent fixes address boot, Wi-Fi, IMS receiver registration, camera database links, audio compatibility and both identified MTK Codec2 crashes. Boot with SELinux enforcing, Wi-Fi and Power/AOD have been checked on the device. Hardware validation is still incomplete, including mobile-network/VoLTE coverage, DRM, all camera modes and battery consumption.

Camera application selection is left to the ROM maintainer. This branch does not import MiCam or require a MiCam vendor tree; maintainers can integrate their chosen camera separately.

The stock kernel, DTB, DTBO and 516 module files are pinned by hashes. Vendor extraction validates the selected EEA blobs and applies guarded compatibility fixes. See [Codec2 notes](patches/CODEC2-ANDROID17.md) and [Power/AOD notes](patches/POWER-AOD.md) for the implementation and validation limits.

## Build on Linux

Use a Linux x86_64 build host with the dependencies described in the [PixelOS build guide](https://blog.pixelos.net/docs/maintainers/guide/building-pixelos/).

### 1. Sync PixelOS and device dependencies

```bash
repo init -u https://github.com/PixelOS-AOSP/android_manifest.git -b seventeen --git-lfs
repo sync

git clone -b pixelos-17 https://github.com/mt6897-degas/android_device_xiaomi_degas.git device/xiaomi/degas
mkdir -p .repo/local_manifests
cp device/xiaomi/degas/degas.xml .repo/local_manifests/degas.xml
repo sync
```

The local manifest pins the required MediaTek, Xiaomi and vendor SELinux projects. PixelOS already supplies the other common dependencies.

### 2. Prepare the matching kernel and proprietary vendor files

Obtain the Xiaomi fastboot package **OS3.0.306.0.WNEEUXM**. Install `fsck.erofs` and `lz4`, then prepare the stock dump and kernel in new output directories:

```bash
python3 device/xiaomi/degas/tools/prepare-stock.py \
    /absolute/path/to/degas_eea_global_images_OS3.0.306.0.WNEEUXM_16.0 \
    --work "$PWD/stock/degas" \
    --kernel "$PWD/device/xiaomi/degas-kernel"

device/xiaomi/degas/tools/extract-vendor.sh "$PWD/stock/degas/dump"
```

This creates `device/xiaomi/degas-kernel` from matching factory files and generates `vendor/xiaomi/degas`. If these directories are already prepared, validate and reuse them instead of recreating them. Preserve the partition-specific kernel module layout, including the different factory zram variants. Do not substitute another device's super geometry or kernel.

### 3. Apply the platform patches and build

```bash
python3 device/xiaomi/degas/tools/apply-patches.py --check
python3 device/xiaomi/degas/tools/apply-patches.py
source build/envsetup.sh
breakfast degas userdebug
m -j$(nproc) updatepackage pixelos
```

The product is **`custom_degas`**. The active five-patch Android 17 series covers UDFPS refresh voting, suspended-display modesets and the MTK gen4m WPA3 compatibility path. The applier checks the complete series before modifying platform files and supports already-applied patches. Recheck after updating the ROM sources. Historical Lineage patches are retained for attribution under `patches/lineage23-reference`; see [the patch guide](patches/README.md).

## Validation

Run from the Android checkout root, with the matching kernel and generated vendor trees available:

```bash
python3 device/xiaomi/degas/tools/validate-tree.py
python3 device/xiaomi/degas/tools/validate-tree.py --stock "$PWD/stock/degas/dump" --vendor
python3 device/xiaomi/degas/verify-hand-edits.py
python3 device/xiaomi/degas/tools/apply-patches.py --check
```

These checks validate XML/Python syntax, the product, kernel/blob hashes, generated vendor paths, guarded blob edits and patch applicability. Android/Soong, ELF, VINTF and combined SELinux checks must also pass during the build; device testing remains necessary.

Use the normal Android OTA tools to generate signed packages. If repacking payload operations separately, use an XZ mode supported by recovery's `xz-embedded`; the original OTA uses `CHECK_NONE`. Python `lzma` defaults to CRC64, which this recovery rejects with `kDownloadOperationExecutionError` / error 28. A desktop liblzma-only verification does not detect that incompatibility.

## Credits and license

- **[Mikhail Mlhcnn (Advnirr)](https://github.com/Advnirr)** — original Xiaomi 14T / degas device tree.
- **[Degas Developers](https://github.com/degas-developers)** — original LineageOS degas tree.
- **[mt6897-devs](https://github.com/mt6897-devs/device_xiaomi_duchamp)** and the original contributors — the duchamp platform tree on which degas was based.
- **[LineageOS](https://github.com/LineageOS)** and **[PixelOS](https://github.com/PixelOS-AOSP)** — ROM sources and common device support.

Original copyright and attribution notices are retained. The PixelOS branch preserves the upstream history together with the adaptation commits. See [LICENSE](LICENSE) and [NOTICE](NOTICE); kernel UAPI headers, stock configuration and proprietary components retain their respective licensing. This is an unofficial PixelOS adaptation.
