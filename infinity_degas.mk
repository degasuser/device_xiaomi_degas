#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# The stock Xiaomi face service supplies IFace/default.
TARGET_PROVIDES_FACE_UNLOCK_HAL := true

# Project Infinity X
INFINITY_MAINTAINER := degasuser
TARGET_HAS_UDFPS := true
WITH_GAPPS := true
# device.mk keys erofs system partitions and compressed VAB off WITH_GMS.
WITH_GMS := true

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/xiaomi/degas/device.mk)

# Inherit Project Infinity X phone configuration.
$(call inherit-product, vendor/infinity/config/common_full_phone.mk)

PRODUCT_BRAND := Xiaomi
PRODUCT_DEVICE := degas
PRODUCT_MANUFACTURER := Xiaomi
PRODUCT_MODEL := 2406APNFAG
PRODUCT_NAME := infinity_degas

PRODUCT_CHARACTERISTICS := nosdcard
PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_SYSTEM_PROPERTIES += \
    ro.product.marketname=Xiaomi 14T \
    ro.infinity.soc=MediaTek Dimensity 8300-Ultra \
    ro.infinity.camera=50MP + 50MP + 12MP

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="missi-user 16 BP2A.250605.031.A3 OS3.0.306.0.WNEEUXM release-keys" \
    DeviceProduct=degas_eea
