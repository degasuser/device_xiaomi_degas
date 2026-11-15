#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# PixelOS includes GMS; set this before device.mk selects the VABC configuration.
WITH_GMS := true
# The stock Xiaomi face service supplies IFace/default.
TARGET_PROVIDES_FACE_UNLOCK_HAL := true

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/xiaomi/degas/device.mk)

# Inherit PixelOS phone configuration (also inherits Lineage compatibility).
$(call inherit-product, vendor/custom/config/common_full_phone.mk)

PRODUCT_BRAND := Xiaomi
PRODUCT_DEVICE := degas
PRODUCT_MANUFACTURER := Xiaomi
PRODUCT_MODEL := 2406APNFAG
PRODUCT_NAME := custom_degas

PRODUCT_CHARACTERISTICS := nosdcard
PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="missi-user 16 BP2A.250605.031.A3 OS3.0.306.0.WNEEUXM release-keys" \
    DeviceProduct=degas_eea
