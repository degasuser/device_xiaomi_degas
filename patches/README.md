# LineageOS 24.0 / Android 17 patches

The active platform series is in `lineage24/`. Run `python3 device/xiaomi/degas/tools/apply-patches.py --check` before applying, then run it without `--check`. The entire series is checked in a scratch Git index before any platform file is changed. Repeat runs accept clean, partially applied and fully applied series; incompatible changes are rejected.

| Patch | Project | Purpose |
| --- | --- | --- |
| 0001 | frameworks/base | Hold the configured optical UDFPS refresh rate while its interactive overlay is visible. |
| 0002 | frameworks/native | Reject OFF-panel mode requests using Android 17's synchronized-bundle cleanup. |
| 0003 | external/wpa_supplicant_8 | Preserve RSN version bits supported by MTK gen4m while retaining SAE key management. |
| 0004 | frameworks/native | Block modesets and hardware-vsync resync in OFF/DOZE_SUSPEND. |
| 0005 | frameworks/base | Release the fixed UDFPS vote in idle AOD, wait for the actual mode before illumination and cancel stale scans. |
| 0006 | build/soong | Allow Xiaomi IMS packages in the device's MediaTek boot jars. |

Patches 0001–0005 carry forward the PixelOS 17 fixes and were rebased against the LineageOS 24.0 source files recorded in [../lineage24-source.lock.json](../lineage24-source.lock.json). Patch 0006 carries forward Mikhail Mlhcnn's Xiaomi boot-jar allowlist fix: current LineageOS 24.0 permits MediaTek packages but does not yet permit `com.xiaomi.ims`. All six patches pass clean application and a second, idempotent check on the recorded source snapshots. This does not replace a full Android build or device validation.

IMS receiver patches in `ims-receivers/` are applied separately by `extract-files.py`. Guarded Codec2 edits are also performed during extraction. See [CODEC2-ANDROID17.md](CODEC2-ANDROID17.md) and [POWER-AOD.md](POWER-AOD.md).

`lineage23-reference/` retains the original upstream patches and attribution. It is not an additional series to apply to LineageOS 24.0. The active boot-jar patch is the reviewed carry-forward from that archive. The old sensor patch is unnecessary for the device's one-shot UDFPS sub-HAL. The audio namespace conflict is handled by the renamed device source module. Launcher and flashlight preferences remain the ROM maintainer's choice.

## Project Infinity X 17

`infinity17/` holds the same six patches for Project Infinity X 17. Infinity forks `frameworks/base` and adds MediaTek GHBM dimming, Smart Pixels and UDFPS animations to `UdfpsController`, so 0001 and 0005 are rebased onto that file: the GHBM dimming step and `setIlluminationRequested` move into the deferred pointer-down runnable, and the UDFPS animation is hidden on any finger-up. Patches 0002, 0003, 0004 and 0006 are unchanged copies. `tools/apply-patches.py` selects `infinity17/` when `vendor/infinity` exists.
