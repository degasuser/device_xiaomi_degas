#!/usr/bin/env python3
"""Check the device-specific AIDL HAL entries reported by checkvintf."""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('vendor', type=Path)
parser.add_argument('--matrix', type=Path, default=Path(__file__).resolve().parents[1] / 'framework_compatibility_matrix.xml')
args = parser.parse_args()
matrix = ET.parse(args.matrix).getroot()
assert matrix.tag == 'compatibility-matrix' and matrix.get('type') == 'framework'
matched = 0
for fragment in [
    'manifest_vendor.xiaomi.hardware.aidl.mtdservice.xml',
    'manifest_vendor.xiaomi.hardware.mfidoca.xml',
]:
    manifest = ET.parse(args.vendor / 'proprietary/odm/etc/vintf/manifest' / fragment).getroot()
    for hal in manifest.findall('hal'):
        package = hal.findtext('name')
        version = hal.findtext('version', '1')
        for interface in hal.findall('interface'):
            name = interface.findtext('name')
            for instance in interface.findall('instance'):
                candidates = [h for h in matrix.findall('hal') if h.get('format') == hal.get('format') and h.findtext('name') == package]
                accepted = any(h.findtext('version') == version and any(i.findtext('name') == name and instance.text in [x.text for x in i.findall('instance')] for i in h.findall('interface')) for h in candidates)
                if not accepted:
                    raise SystemExit(f'Missing matching framework matrix entry: {package}.{name}/{instance.text} (AIDL {version})')
                matched += 1
if matched != 2:
    raise SystemExit(f'Expected to check two stock HAL instances, checked {matched}')
print('Device-specific VINTF declarations checked: both stock AIDL v1/default instances match the framework matrix. Full checkvintf remains required.')
