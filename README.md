# Device tree for Xiaomi 14T (degas)

```
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
```

The Xiaomi 14T (codenamed *degas*) is a high-end smartphone from Xiaomi, announced in September 2024.

## Device specifications

| Feature | Specification |
| :--- | :--- |
| Chipset | MediaTek Dimensity 8300-Ultra (4 nm) |
| CPU | Octa-core (1x 3.35 GHz Cortex-A715 & 3x 3.20 GHz Cortex-A715 & 4x 2.20 GHz Cortex-A510) |
| GPU | Mali-G615-MC6 |
| Memory | 12 GB / 16 GB LPDDR5X |
| Storage | 256 GB / 512 GB UFS 4.0 |
| MicroSD | No |
| Battery | 5000 mAh (Li-Po), 67W wired fast charging |
| Dimensions | 160.5 x 75.1 x 7.8 mm |
| Display | 6.67" AMOLED, 1220 x 2712 pixels (446 ppi), 144Hz, HDR10+, Dolby Vision |
| Rear Cameras | 50 MP (wide, Sony IMX906, OIS) + 50 MP (telephoto, Samsung S5KJN1, 2x optical) + 12 MP (ultrawide, Omnivision OV13B) |
| Front Camera | 32 MP (wide, Samsung S5KKD1) |

## Build instructions

### Set up build environment
Follow the official LineageOS build guide to set up your environment.

### Clone the device tree
```bash
git clone https://github.com/degasuser/device_xiaomi_degas.git device/xiaomi/degas
```

### Extract proprietary blobs
From a connected device running stock HyperOS or an extracted ROM dump:
```bash
cd device/xiaomi/degas
./extract-files.py <path_to_stock_dump>
```

### Build LineageOS
```bash
source build/envsetup.sh
breakfast degas
brunch degas
```
