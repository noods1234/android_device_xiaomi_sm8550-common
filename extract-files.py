#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'vendor/qcom/common/system/telephony',
    'vendor/qcom/common/vendor/adreno-t',
    'vendor/qcom/common/vendor/display/5.15',
]

def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_odm' if partition in ('odm', 'vendor') else None

def lib_fixup_sm8550_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_sm8550' if partition in ('odm', 'vendor') else None

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_vendor' if partition in ('odm', 'vendor') else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.xiaomi.hardware.fx.tunnel@1.0',
        'vendor.xiaomi.hardware.mfidoca@1.0',
        'vendor.xiaomi.hardware.mlipay@1.0',
        'vendor.xiaomi.hardware.mlipay@1.1',
        'vendor.xiaomi.hardware.mtdservice@1.0',
        'vendor.xiaomi.hardware.mtdservice@1.1',
        'vendor.xiaomi.hardware.mtdservice@1.2',
        'vendor.xiaomi.hardware.mtdservice@1.3',
        'vendor.xiaomi.hardware.tidaservice@1.0',
        'vendor.xiaomi.hardware.tidaservice@1.1',
        'vendor.xiaomi.hardware.tidaservice@1.2',
    ): lib_fixup_odm_suffix,
    (
        'audio.primary.kalama',
        'libsdm-color',
        'libsdm-disp-vndapis',
        'libsdmextension',
    ): lib_fixup_sm8550_suffix,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'com.qualcomm.qti.imscmservice@1.0',
        'com.qualcomm.qti.imscmservice@2.0',
        'com.qualcomm.qti.imscmservice@2.1',
        'com.qualcomm.qti.imscmservice@2.2',
        'com.qualcomm.qti.uceservice@2.0',
        'com.qualcomm.qti.uceservice@2.1',
        'com.qualcomm.qti.uceservice@2.2',
        'com.qualcomm.qti.uceservice@2.3',
        'vendor.qti.data.factory@2.0',
        'vendor.qti.data.factory@2.1',
        'vendor.qti.data.factory@2.2',
        'vendor.qti.data.factory@2.3',
        'vendor.qti.data.factory@2.4',
        'vendor.qti.data.factory@2.5',
        'vendor.qti.data.factory@2.6',
        'vendor.qti.data.factory@2.7',
        'vendor.qti.data.mwqem@1.0',
        'vendor.qti.data.slm@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.data.cne.internal.api@1.0',
        'vendor.qti.hardware.data.cne.internal.constants@1.0',
        'vendor.qti.hardware.data.cne.internal.server@1.0',
        'vendor.qti.hardware.data.cne.internal.server@1.1',
        'vendor.qti.hardware.data.cne.internal.server@1.2',
        'vendor.qti.hardware.data.cne.internal.server@1.3',
        'vendor.qti.hardware.data.connection@1.0',
        'vendor.qti.hardware.data.connection@1.1',
        'vendor.qti.hardware.data.connectionfactory-V1-ndk',
        'vendor.qti.hardware.data.dataactivity-V1-ndk',
        'vendor.qti.hardware.data.dynamicdds@1.0',
        'vendor.qti.hardware.data.dynamicdds@1.1',
        'vendor.qti.hardware.data.flow@1.0',
        'vendor.qti.hardware.data.flow@1.1',
        'vendor.qti.hardware.data.iwlan@1.0',
        'vendor.qti.hardware.data.iwlan@1.1',
        'vendor.qti.hardware.data.ka-V1-ndk',
        'vendor.qti.hardware.data.latency@1.0',
        'vendor.qti.hardware.data.lce@1.0',
        'vendor.qti.hardware.data.qmi@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.dpmservice@1.1',
        'vendor.qti.hardware.embmssl@1.0',
        'vendor.qti.hardware.embmssl@1.1',
        'vendor.qti.hardware.limits@1.0',
        'vendor.qti.hardware.limits@1.1',
        'vendor.qti.hardware.limits@1.2',
        'vendor.qti.hardware.ListenSoundModel@1.0',
        'vendor.qti.hardware.mwqemadapter@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.hardware.qxr-V1-ndk',
        'vendor.qti.hardware.radio.am-V1-ndk',
        'vendor.qti.hardware.radio.am@1.0',
        'vendor.qti.hardware.radio.atcmdfwd-V1-ndk',
        'vendor.qti.hardware.radio.atcmdfwd@1.0',
        'vendor.qti.hardware.radio.ims-V9-ndk',
        'vendor.qti.hardware.radio.ims@1.0',
        'vendor.qti.hardware.radio.ims@1.1',
        'vendor.qti.hardware.radio.ims@1.2',
        'vendor.qti.hardware.radio.ims@1.3',
        'vendor.qti.hardware.radio.ims@1.4',
        'vendor.qti.hardware.radio.ims@1.5',
        'vendor.qti.hardware.radio.ims@1.6',
        'vendor.qti.hardware.radio.ims@1.7',
        'vendor.qti.hardware.radio.ims@1.8',
        'vendor.qti.hardware.radio.internal.deviceinfo-V1-ndk',
        'vendor.qti.hardware.radio.internal.deviceinfo@1.0',
        'vendor.qti.hardware.radio.lpa@1.0',
        'vendor.qti.hardware.radio.lpa@1.1',
        'vendor.qti.hardware.radio.lpa@1.2',
        'vendor.qti.hardware.radio.lpa@1.3',
        'vendor.qti.hardware.radio.qcrilhook-V1-ndk',
        'vendor.qti.hardware.radio.qcrilhook@1.0',
        'vendor.qti.hardware.radio.qtiradio-V9-ndk',
        'vendor.qti.hardware.radio.qtiradio@1.0',
        'vendor.qti.hardware.radio.qtiradio@2.0',
        'vendor.qti.hardware.radio.qtiradio@2.1',
        'vendor.qti.hardware.radio.qtiradio@2.2',
        'vendor.qti.hardware.radio.qtiradio@2.3',
        'vendor.qti.hardware.radio.qtiradio@2.4',
        'vendor.qti.hardware.radio.qtiradio@2.5',
        'vendor.qti.hardware.radio.qtiradio@2.6',
        'vendor.qti.hardware.radio.qtiradioconfig-V3-ndk',
        'vendor.qti.hardware.radio.uim@1.0',
        'vendor.qti.hardware.radio.uim@1.1',
        'vendor.qti.hardware.radio.uim@1.2',
        'vendor.qti.hardware.radio.uim_remote_client@1.0',
        'vendor.qti.hardware.radio.uim_remote_client@1.1',
        'vendor.qti.hardware.radio.uim_remote_client@1.2',
        'vendor.qti.hardware.radio.uim_remote_server@1.0',
        'vendor.qti.hardware.sigma_miracast@1.0',
        'vendor.qti.hardware.slmadapter@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ims.callcapability@1.0',
        'vendor.qti.ims.callinfo@1.0',
        'vendor.qti.ims.configservice@1.0',
        'vendor.qti.ims.configservice@1.1',
        'vendor.qti.ims.connection@1.0',
        'vendor.qti.ims.factory@1.0',
        'vendor.qti.ims.factory@1.1',
        'vendor.qti.ims.factory@2.0',
        'vendor.qti.ims.factory@2.1',
        'vendor.qti.ims.factory@2.2',
        'vendor.qti.ims.rcsconfig@1.0',
        'vendor.qti.ims.rcsconfig@1.1',
        'vendor.qti.ims.rcsconfig@2.0',
        'vendor.qti.ims.rcsconfig@2.1',
        'vendor.qti.ims.rcssip@1.0',
        'vendor.qti.ims.rcssip@1.1',
        'vendor.qti.ims.rcssip@1.2',
        'vendor.qti.ims.rcsuce@1.0',
        'vendor.qti.ims.rcsuce@1.1',
        'vendor.qti.ims.rcsuce@1.2',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.latency@2.0',
        'vendor.qti.latency@2.1',
        'vendor.qti.latency@2.2',
        'vendor.qti.latency@2.3',
        'vendor.xiaomi.hardware.displayfeature@1.0',
        'vendor.xiaomi.hardware.fingerprintextension@1.0',
    ): lib_fixup_vendor_suffix,
    (
        'libcamxcommonutils',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'odm/lib64/hw/displayfeature.default.so',
        'vendor/lib64/hw/audio.primary.kalama.so',
    ): blob_fixup()
        .replace_needed(
            'libstagefright_foundation.so',
            'libstagefright_foundation-v33.so',
        ),
    'odm/lib64/libmt@1.3.so': blob_fixup()
        .replace_needed(
            'libcrypto.so',
            'libcrypto-v33.so',
        ),
    'system_ext/framework/mirilhook.jar': blob_fixup()
        .apktool_patch('blob-patches/mirilhook.patch', '-r'),
    # modemManager embeds SHA-256 fingerprints of its QESDK (Qualcomm E-Commerce SDK)
    # dependency libraries and validates them at runtime.  libqesdk2_0.so and
    # libqesdk_manager.so are carrier/commercial SDK blobs not present in AOSP
    # builds; leaving the fingerprints intact causes modemManager to abort with a
    # dlopen / integrity-check failure on first use.  Replacing each hash with
    # SHA-256("") (the canonical null fingerprint) disables the check and allows
    # modemManager to start without those libraries.
    #
    # Fragility note: these hashes are embedded as literal byte strings in the
    # binary; if modemManager is relinked in a future Xiaomi blob drop the offsets
    # may shift and binary_regex_replace will silently miss.  Symptom: modemManager
    # crashes at boot with "library not found" or integrity failure.
    # Verification: after extraction run
    #   grep -c <original_hash_hex> vendor/bin/modemManager
    # and confirm output is 0 (replaced); non-zero means the fixup missed.
    'vendor/bin/modemManager' : blob_fixup()
        .binary_regex_replace(b'fbec992f7f41a65ac8000aeda1bc634e24a12c7513faae379ae889a53553325a', b'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')  # libqesdk2_0.so fingerprint → SHA-256("")
        .binary_regex_replace(b'40821d2c697710a692462776324a4b913935878b3b5f2232a2cd297a6f3ff37f', b'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'), # libqesdk_manager.so fingerprint → SHA-256("")
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    # Cinema media profiles patch: inserts CamcorderProfiles blocks for both cameras
    # before the stock Qualcomm blocks so the first-match parser in MediaProfiles.java
    # returns cinema specs (HEVC, high bitrate) for shared quality names (2160p, 1080p).
    #
    # Failure modes:
    #   Hunk mismatch (stock XML changed in a new Xiaomi drop) → patch(1) returns non-zero
    #     and extraction aborts with "Hunk FAILED at …"; fix by regenerating the patch
    #     against the new stock file: diff -u stock.xml patched.xml > media_profiles_cinema.patch
    #   HAL ignores unsupported profiles at runtime (no error, profile silently absent) →
    #     verify with: adb shell dumpsys media.camera | grep -i profile
    #     or check logcat tag MediaProfiles after first camera open.
    #   Sentinel check after extraction (confirms patch landed):
    #     grep -c '4kdci' vendor/xiaomi/sm8550-common/vendor/etc/media_profiles_kalama.xml
    #     must return ≥ 1; zero means the file was replaced post-patch or patch missed.
    'vendor/etc/media_profiles_kalama.xml': blob_fixup()
        .patch_file('blob-patches/media_profiles_cinema.patch'),
    'vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy': blob_fixup()
        .add_line_if_missing('setsockopt: 1'),
    'vendor/etc/seccomp_policy/qwesd@2.0.policy': blob_fixup()
        .add_line_if_missing('pipe2: 1'),
    'vendor/lib64/c2.dolby.client.so': blob_fixup()
        .add_needed('libcodec2_hidl_shim.so'),
    'vendor/lib64/libsnpe_config.so': blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8550-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
