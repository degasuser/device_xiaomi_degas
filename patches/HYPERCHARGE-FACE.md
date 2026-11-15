# Degas charging and face enrollment compatibility

The stock input is OS3.0.306.0.WNEEUXM. These changes fix two confirmed
integration problems. Charging power and completed enrollment still require
hardware verification; no new device measurements are claimed.

## Accelerated charging

Stock `batterysecret` initializes its acceleration feature to one, then clears
it in the `degas` device branch. `verify_pd_digest()` consequently forces
`persist.vendor.accelerate.charge=false`, overriding the existing init default.
Saved degas logs confirm both `accelerate_charge:0` and the false property.

`tools/hypercharge_compat.py` changes `sturh wzr, [x19, #0x31]` to
`sturb wzr, [x19, #0x31]`. Reverse authentication stays disabled for degas;
acceleration stays enabled. Battery/charger digest verification, Xiaomi VDM
negotiation, EEA detection, smart-sense and kernel limits are unchanged.
The fix rejects every unrecognized input hash and is idempotent. Run:

```sh
python3 device/xiaomi/degas/tools/test_hypercharge.py \
  /path/to/stock/vendor/bin/batterysecret
```

The init property also repairs the persistent false value from older builds.
This restores the accelerated charging path; it does not guarantee a particular
wattage with any cable, charger, battery level or temperature.

## Face enrollment

The Xiaomi AIDL v3 HAL owns the front camera and accepts a preview native handle
in `enrollWithContext`. Its startup and trusted application load already succeed.
Both matching Android 17 Settings sources provide
`config_face_enroll_hal_owns_camera`, but default it to false. Degas previously
had no override: Settings opened a competing camera and passed a null preview.

The Settings overlay enables that option, so enrollment waits for a valid
Surface and passes it to the HAL. Its 640 x 480 preview is a supported front
camera PRIVATE/YUV output in the saved camera metadata. AIDL v3 already selects
`enrollWithContext`; no interface version spoofing or biometric-strength changes
are needed. No template, TEE, authentication-token or SELinux bypass is added.

The native camera client also needs camera callbacks in the reverse Binder
direction. `binder_call(hal_face_default, cameraserver)` only allowed reverse
transfer; it did not allow `cameraserver` to call the face client's listeners.
The stock Xiaomi domain had that access through `binderservicedomain`, whereas
the AOSP face domain does not. Add the explicit camera-to-face call and FD use,
camera attribution reads, HIDL preview token lookup and gralloc client access.
These are limited to the native camera path and retain SELinux enforcement.
The compiled policy was checked with neverallow assertions enabled; a native
host compiler first reproduced the installed policy byte for byte. Effective
binary-policy queries confirmed the previously denied camera accesses now work.

Source references: PixelOS Settings `752694e6e1a32fc744aca9b65f0b4d8ea2a58f01`,
LineageOS Settings `31b1a9f1cab9638bc6af9f4e6412fbf3b3a7947a`,
`FaceEnrollPreviewFragment.java`, `FaceEnrollEnrolling.java`, and
`res/values/custom_config.xml`.
