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
comparisons, 991 native dependency declarations and 20 firmware hash checks,
with no errors. The OTA firmware list excludes the old preloader and logo.
