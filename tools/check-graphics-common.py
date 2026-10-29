#!/usr/bin/env python3
"""Check vendor graphics.common AIDL imports after extraction fixups."""
import argparse
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('vendor', type=Path, help='Path to vendor/xiaomi/degas')
args = parser.parse_args()
blueprint = (args.vendor / 'Android.bp').read_text()
interface = re.compile(r'android\.hardware\.graphics\.common-V(\d+)-ndk(?:\.so)?$')
errors = []
for name in re.findall(r'"([^"]+)"', blueprint):
    match = interface.fullmatch(name)
    if match and match[1] != '7':
        errors.append(f'Blueprint imports incompatible {name}; this tree uses graphics.common V7')

checked = 0
for source in sorted(set(re.findall(r'"(proprietary/[^"\n]+)"', blueprint))):
    path = args.vendor / source
    if not path.is_file():
        errors.append(f'Missing prebuilt: {source}')
        continue
    with path.open('rb') as stream:
        if stream.read(4) != b'\x7fELF':
            continue
    dynamic = subprocess.check_output(['readelf', '-dW', str(path)], text=True)
    for dependency in re.findall(r'\(NEEDED\).*\[([^]]+)\]', dynamic):
        match = interface.fullmatch(dependency)
        if not match:
            continue
        checked += 1
        if match[1] != '7':
            errors.append(f'{source}: DT_NEEDED imports {dependency}; expected graphics.common V7')
if not checked:
    errors.append('No graphics.common imports checked')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Graphics AIDL check passed: {checked} ELF imports and Blueprint references use graphics.common V7.')
