#!/usr/bin/env python3
"""Check the prebuilt kernel header archive and all known degas consumers."""
import argparse
from pathlib import Path
import tarfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('top', type=Path, help='Android source root, after apply-build-patches.sh')
args = parser.parse_args()
archive = args.top / 'device/xiaomi/degas-kernel/kernel-uapi-headers.tar.gz'
required = {
    'usr/include/asm/signal.h',
    'usr/include/asm-generic/signal.h',
    'usr/include/linux/ioctl.h',
    'usr/include/linux/xiaomi_touch.h',
    'usr/include/drm/mi_disp.h',
}
with tarfile.open(archive, 'r:gz') as headers:
    members = {entry.name.removeprefix('./'): entry for entry in headers.getmembers()}
    for name in required:
        if name not in members or not members[name].isfile() or members[name].size == 0:
            raise SystemExit(f'Missing or empty kernel header: {name}')

for name in [
    'device/xiaomi/degas/udfps/Android.bp',
    'device/xiaomi/degas/sensors/Android.bp',
    'hardware/xiaomi/fingerprint/Android.bp',
    'hardware/mediatek/packages/PowerOffAlarm/Android.bp',
]:
    source = (args.top / name).read_text()
    if '"generated_kernel_headers"' in source or '"prebuilt_kernel_headers"' not in source:
        raise SystemExit(f'{name}: expected prebuilt_kernel_headers; apply the device build patches')
print('Prebuilt kernel header checks passed: archive, five required headers and four consumers.')
