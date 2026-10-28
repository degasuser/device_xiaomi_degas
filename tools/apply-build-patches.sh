#!/bin/bash
# Run from the Android source root, or supply that root as the first argument.
set -euo pipefail
android_top="$(cd "${1:-$PWD}" && pwd)"
patch_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../build/patches" && pwd)"
for hardware in mediatek xiaomi; do
    repository="$android_top/hardware/$hardware"
    patch="$patch_dir/hardware-$hardware-prebuilt-headers.patch"
    if git -C "$repository" apply --reverse --check "$patch" >/dev/null 2>&1; then
        echo "Prebuilt kernel headers already selected in hardware/$hardware"
    else
        git -C "$repository" apply --check "$patch"
        git -C "$repository" apply "$patch"
        echo "Selected prebuilt kernel headers in hardware/$hardware"
    fi
done
