#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# The stock Xiaomi face service supplies IFace/default, so crDroid's
# camera-based FaceUnlock app stays out.
TARGET_PROVIDES_FACE_UNLOCK_HAL := true
TARGET_FACE_UNLOCK_SUPPORTED := false

# Bundled GApps. device.mk keys erofs system partitions and compressed VAB off WITH_GMS.
WITH_GMS := true

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/xiaomi/degas/device.mk)

# Inherit crDroid (vendor/lineage) phone configuration.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Bundled Google apps (vendor/pixel/gms, synced by the local manifest).
$(call inherit-product, vendor/pixel/gms/products/gms.mk)

PRODUCT_BRAND := Xiaomi
PRODUCT_DEVICE := degas
PRODUCT_MANUFACTURER := Xiaomi
PRODUCT_MODEL := 2406APNFAG
PRODUCT_NAME := lineage_degas

PRODUCT_CHARACTERISTICS := nosdcard
PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="missi-user 16 BP2A.250605.031.A3 OS3.0.306.0.WNEEUXM release-keys" \
    DeviceProduct=degas_eea
