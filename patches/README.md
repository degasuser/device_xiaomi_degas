# PixelOS 17 patches

The platform patch applier uses `pixelos17/`. IMS receiver patches under `ims-receivers/` are applied separately by `extract-files.py`. Run `python3 device/xiaomi/degas/tools/apply-patches.py --check` before applying, then run it without `--check`. The complete five-patch series is checked in a scratch Git index before any mutation, including overlapping incremental patches. Repeat runs accept already-applied patches. Recheck after syncing or changing upstream sources.

| Patch | Project | Purpose |
| --- | --- | --- |
| 0001 | frameworks/base | Keep optical UDFPS at 120 Hz for its overlay session. The same display-mode provider is retained for release. |
| 0002 | frameworks/native | Reject mode requests on OFF panels through Android 17's existing synchronized-bundle cleanup. DOZE remains powered on. |
| 0003 | external/wpa_supplicant_8 | For the configured MTK gen4m driver, use the supported RSN WPA-version bit while preserving SAE key management. |
| 0004 | frameworks/native | Reject suspended-panel modesets and hardware-vsync resync in OFF/DOZE_SUSPEND. |
| 0005 | frameworks/base | Release the fixed UDFPS rate in idle AOD; confirm the actual mode before illumination and cancel stale scans. |

Patches 0001–0003 were included in the initial 2026-11-13 ROM; subsequent boot and connectivity fixes are documented in the workspace memory. Patches 0004–0005 were applied to the same pinned sources on 2026-11-14. The targeted build and on-device Power/AOD installation completed; battery consumption remains unmeasured. See [POWER-AOD.md](POWER-AOD.md) for power changes and verification limits. Future upstream changes may require rebasing.

The `lineage23-reference/` directories retain upstream patches for attribution and investigation. Do not apply them to PixelOS 17: some are obsolete, some target changed code, and the Xiaomi boot-jar allowlist entry is already present in PixelOS 17. The audio namespace conflict is solved in the device tree by renaming its source module while retaining the executable stem. The old Launcher3 patch does not configure the prebuilt Pixel Launcher.
