#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# verify-blobs.sh — post-extraction sanity checks for sm8550-common blob fixups.
#
# Run from the device tree root after ./extract-files.py completes:
#   ./verify-blobs.sh
#
# Exits 0 if all checks pass, 1 if any fail.  Designed to be wired into CI
# as a post-extraction step.
#

set -euo pipefail

VENDOR_PATH="../../../vendor/xiaomi/sm8550-common/proprietary"
PASS=0
FAIL=0

pass() { echo "PASS  $1"; ((PASS++)); }
fail() { echo "FAIL  $1"; ((FAIL++)); }

require_file() {
    local f="$VENDOR_PATH/$1"
    if [[ ! -f "$f" ]]; then
        echo "SKIP  $2 (file not found: $f)"
        return 1
    fi
    return 0
}

# ---------------------------------------------------------------------------
# modemManager: QESDK SHA-256 fingerprints replaced with SHA-256("")
# binary_regex_replace patches ASCII hex strings in-place; grep -ca counts
# occurrences in binary-as-text.
# ---------------------------------------------------------------------------
MODEM="$VENDOR_PATH/vendor/bin/modemManager"
if [[ -f "$MODEM" ]]; then
    c=$(grep -ca "fbec992f7f41a65ac8000aeda1bc634e24a12c7513faae379ae889a53553325a" "$MODEM" 2>/dev/null || true)
    [[ "$c" == "0" ]] && pass "modemManager: libqesdk2_0.so fingerprint nulled" \
                        || fail "modemManager: libqesdk2_0.so fingerprint still present (count=$c)"

    c=$(grep -ca "40821d2c697710a692462776324a4b913935878b3b5f2232a2cd297a6f3ff37f" "$MODEM" 2>/dev/null || true)
    [[ "$c" == "0" ]] && pass "modemManager: libqesdk_manager.so fingerprint nulled" \
                        || fail "modemManager: libqesdk_manager.so fingerprint still present (count=$c)"
else
    echo "SKIP  modemManager checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# media_profiles_kalama.xml: cinema patch applied — 4kdci profile must exist
# ---------------------------------------------------------------------------
PROFILES="$VENDOR_PATH/vendor/etc/media_profiles_kalama.xml"
if [[ -f "$PROFILES" ]]; then
    c=$(grep -c "4kdci" "$PROFILES" 2>/dev/null || true)
    [[ "$c" -ge 1 ]] && pass "media_profiles_kalama.xml: 4kdci cinema profile present (count=$c)" \
                      || fail "media_profiles_kalama.xml: cinema patch missing (4kdci not found)"
else
    echo "SKIP  media_profiles checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# audio.primary.kalama.so: libstagefright_foundation → -v33 replace_needed
# ---------------------------------------------------------------------------
AUD="$VENDOR_PATH/vendor/lib64/hw/audio.primary.kalama.so"
if [[ -f "$AUD" ]]; then
    c=$(strings "$AUD" | grep -c "libstagefright_foundation-v33.so" || true)
    [[ "$c" -ge 1 ]] && pass "audio.primary.kalama.so: libstagefright_foundation-v33 DT_NEEDED" \
                      || fail "audio.primary.kalama.so: libstagefright_foundation-v33 DT_NEEDED missing"

    c=$(strings "$AUD" | grep -c "^libstagefright_foundation\.so$" || true)
    [[ "$c" == "0" ]] && pass "audio.primary.kalama.so: old libstagefright_foundation.so removed" \
                       || fail "audio.primary.kalama.so: old libstagefright_foundation.so still in DT_NEEDED"
else
    echo "SKIP  audio.primary.kalama.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# displayfeature.default.so: same replace_needed
# ---------------------------------------------------------------------------
DISP="$VENDOR_PATH/odm/lib64/hw/displayfeature.default.so"
if [[ -f "$DISP" ]]; then
    c=$(strings "$DISP" | grep -c "libstagefright_foundation-v33.so" || true)
    [[ "$c" -ge 1 ]] && pass "displayfeature.default.so: libstagefright_foundation-v33 DT_NEEDED" \
                      || fail "displayfeature.default.so: libstagefright_foundation-v33 DT_NEEDED missing"
else
    echo "SKIP  displayfeature.default.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# libmt@1.3.so: libcrypto → -v33 replace_needed
# ---------------------------------------------------------------------------
MT="$VENDOR_PATH/odm/lib64/libmt@1.3.so"
if [[ -f "$MT" ]]; then
    c=$(strings "$MT" | grep -c "libcrypto-v33.so" || true)
    [[ "$c" -ge 1 ]] && pass "libmt@1.3.so: libcrypto-v33 DT_NEEDED" \
                      || fail "libmt@1.3.so: libcrypto-v33 DT_NEEDED missing"
else
    echo "SKIP  libmt@1.3.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# keymint service + library: RKP shim add_needed
# ---------------------------------------------------------------------------
KM_SVC="$VENDOR_PATH/vendor/bin/hw/android.hardware.security.keymint-service-qti"
if [[ -f "$KM_SVC" ]]; then
    c=$(strings "$KM_SVC" | grep -c "android.hardware.security.rkp-V3-ndk.so" || true)
    [[ "$c" -ge 1 ]] && pass "keymint-service-qti: rkp-V3-ndk DT_NEEDED" \
                      || fail "keymint-service-qti: rkp-V3-ndk DT_NEEDED missing"
else
    echo "SKIP  keymint-service-qti checks (not extracted)"
fi

KM_LIB="$VENDOR_PATH/vendor/lib64/libqtikeymint.so"
if [[ -f "$KM_LIB" ]]; then
    c=$(strings "$KM_LIB" | grep -c "android.hardware.security.rkp-V3-ndk.so" || true)
    [[ "$c" -ge 1 ]] && pass "libqtikeymint.so: rkp-V3-ndk DT_NEEDED" \
                      || fail "libqtikeymint.so: rkp-V3-ndk DT_NEEDED missing"
else
    echo "SKIP  libqtikeymint.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# c2.dolby.client.so: codec2 shim add_needed
# ---------------------------------------------------------------------------
DOLBY="$VENDOR_PATH/vendor/lib64/c2.dolby.client.so"
if [[ -f "$DOLBY" ]]; then
    c=$(strings "$DOLBY" | grep -c "libcodec2_hidl_shim.so" || true)
    [[ "$c" -ge 1 ]] && pass "c2.dolby.client.so: libcodec2_hidl_shim DT_NEEDED" \
                      || fail "c2.dolby.client.so: libcodec2_hidl_shim DT_NEEDED missing"
else
    echo "SKIP  c2.dolby.client.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# libsnpe_config.so: liblog add_needed
# ---------------------------------------------------------------------------
SNPE="$VENDOR_PATH/vendor/lib64/libsnpe_config.so"
if [[ -f "$SNPE" ]]; then
    c=$(strings "$SNPE" | grep -c "liblog.so" || true)
    [[ "$c" -ge 1 ]] && pass "libsnpe_config.so: liblog DT_NEEDED" \
                      || fail "libsnpe_config.so: liblog DT_NEEDED missing"
else
    echo "SKIP  libsnpe_config.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# vendor.libdpmframework.so: hidlbase shim add_needed
# ---------------------------------------------------------------------------
DPM="$VENDOR_PATH/vendor/lib64/vendor.libdpmframework.so"
if [[ -f "$DPM" ]]; then
    c=$(strings "$DPM" | grep -c "libhidlbase_shim.so" || true)
    [[ "$c" -ge 1 ]] && pass "vendor.libdpmframework.so: libhidlbase_shim DT_NEEDED" \
                      || fail "vendor.libdpmframework.so: libhidlbase_shim DT_NEEDED missing"
else
    echo "SKIP  vendor.libdpmframework.so checks (not extracted)"
fi

# ---------------------------------------------------------------------------
# seccomp policies: required syscalls present
# ---------------------------------------------------------------------------
C2POL="$VENDOR_PATH/vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy"
if [[ -f "$C2POL" ]]; then
    grep -q "setsockopt: 1" "$C2POL" \
        && pass "c2audio seccomp policy: setsockopt present" \
        || fail "c2audio seccomp policy: setsockopt missing"
else
    echo "SKIP  c2audio seccomp policy (not extracted)"
fi

QWES="$VENDOR_PATH/vendor/etc/seccomp_policy/qwesd@2.0.policy"
if [[ -f "$QWES" ]]; then
    grep -q "pipe2: 1" "$QWES" \
        && pass "qwesd seccomp policy: pipe2 present" \
        || fail "qwesd seccomp policy: pipe2 missing"
else
    echo "SKIP  qwesd seccomp policy (not extracted)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[[ "$FAIL" == "0" ]]
