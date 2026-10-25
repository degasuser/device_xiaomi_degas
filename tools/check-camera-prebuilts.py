#!/usr/bin/env python3
"""Check sensor module definitions, ELF names and tuning data without an AOSP build."""
import argparse
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('vendor', type=Path, help='Path to vendor/xiaomi/degas')
args = parser.parse_args()
errors = []
blueprint = (args.vendor / 'Android.bp').read_text()
modules = {}
for block in re.split(r'\n(?=\w+\s*\{)', blueprint):
    name = re.search(r'\bname:\s*"([^"]+)"', block)
    if name:
        modules[name[1]] = block

sensor = re.compile(r'^(?:degas|duchamp).+_(?:IdxMgr|tuning)$')
checked = 0
for name, block in modules.items():
    if not block.lstrip().startswith('cc_prebuilt_'):
        continue
    for dependencies in re.findall(r'shared_libs:\s*\[(.*?)\]', block, re.S):
        for dependency in re.findall(r'"([^"]+)"', dependencies):
            if sensor.match(dependency) and dependency not in modules:
                errors.append(f'{name}: undefined camera module {dependency}')
    if not sensor.match(name):
        continue
    source = re.search(r'"(proprietary/[^"\n]+\.so)"', block)
    if not source:
        errors.append(f'{name}: no library source')
        continue
    path = args.vendor / source[1]
    if not path.is_file():
        errors.append(f'{name}: missing {path}')
        continue
    dynamic = subprocess.check_output(['readelf', '-dW', str(path)], text=True)
    soname = re.search(r'\(SONAME\).*\[([^]]+)\]', dynamic)
    if not soname or soname[1] != name + '.so':
        errors.append(f'{name}: SONAME does not match module name')
    for dependency in re.findall(r'\(NEEDED\).*\[([^]]+)\]', dynamic):
        dependency = dependency.removesuffix('.so')
        if sensor.match(dependency) and dependency not in modules:
            errors.append(f'{name}: unresolved DT_NEEDED {dependency}')
    checked += 1

for model in ['degasimx906wide', 'degass5kkd1front', 'degass5kjn1tele', 'degasov13b10ultra']:
    prefix = model + '_mipi_raw'
    for suffix in ['_IdxMgr', '_tuning']:
        if prefix + suffix not in modules:
            errors.append(f'Missing Xiaomi 14T sensor library: {prefix + suffix}')
    for filename in ['ISP_mapping.db', 'ISP_param.db']:
        path = args.vendor / 'proprietary/odm/bin/crossbuild/DataSet/SQLiteModule/db/tuning_DB' / prefix / 'mt6897' / filename
        if not path.is_file():
            errors.append(f'Missing tuning database: {path}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'Camera prebuilt checks passed: {checked} libraries, all sensor dependencies defined; four degas sensor tuning sets present.')
