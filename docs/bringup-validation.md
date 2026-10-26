# Degas prebuilt bringup validation

Firmware base: HyperOS **OS3.0.303.0.WNERUXM** for Xiaomi 14T (`degas`).
Use the device, vendor and prebuilt kernel changes together.

The Soong failure for `libbase-v34` is fixed by changing the extraction fixup
and the actual KeyMint blob dependency to `libbase-v33`. The two libbase
symbols imported by the blob are exported by the arm64 compat library.

Regenerate vendor makefiles after applying blob fixups. `shared_libs` must
match `DT_NEEDED`; changing the Blueprint alone cannot repair a runtime link
failure. The IMS receiver patch is rebased on the matching stock APK.

The local manifest includes MediaTek vendor sepolicy and avoids adding a
second `hardware/lineage/interfaces` project, which LineageOS already provides.

Before flashing, validate the combined changes in a complete LineageOS checkout:

```sh
source build/envsetup.sh
breakfast degas
m nothing
m bacon
```

The isolated prebuilt audit checks module load-list coverage, dependencies in
the combined normal/recovery ramdisk, module-to-module symbol CRCs, native
prebuilt dependency declarations, source-file existence and firmware hashes.
These checks do not replace a full Soong/VINTF build or a device boot test.
The current BoardConfig retains the existing permissive SELinux bringup mode.

Stock refresh: 1,374 listed inputs were copied from this archive; 384 existing
compatibility inputs were retained because their source paths are absent in
this ROM. These include older camera compatibility libraries. Their presence
is not a runtime compatibility guarantee; review the complete build ELF checks
and device logs before treating this tree as boot-tested.

The prebuilt audit completed with 492 kernel modules, 3,837 module symbol CRC
comparisons, 1,001 native dependency declarations and 20 firmware hash checks,
with no errors. The OTA firmware list excludes the old preloader and logo.

Camera inventory follow-up: restored 28 stock sensor libraries and 11 tuning
database files, preserving the original duchamp and degas names required by
the stock HAL. Verify module definitions, SONAME/DT_NEEDED and the four Xiaomi
14T sensor data sets with:

```sh
python3 device/xiaomi/degas/tools/check-camera-prebuilts.py vendor/xiaomi/degas
```

The regression check rejects the previous Blueprint with undefined camera
modules. The previous ELF audit alone did not check module existence.

Graphics AIDL follow-up: stock PQ V7 imports graphics.common V4, conflicting
with platform libui/libgralloctypes (V7). Include PQ V7 in the existing V4-to-V7
ELF fixup group and regenerate its Blueprint. Only the dependency name changes
in the blob; function code and file size are unchanged. The fresh-stock fixup
is idempotent. The local checker validates 14 graphics.common ELF imports and
Blueprint references and rejects the previous V4 Blueprint:

```sh
python3 device/xiaomi/degas/tools/check-graphics-common.py vendor/xiaomi/degas
```

The complete Soong graph still requires a remote build; these checks do not
prove runtime ABI compatibility.
