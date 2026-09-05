/*
 * SPDX-FileCopyrightText: WitAqua
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

/*
 * wifi_hal_fn layout shim for the Android 15 era vendor blob.
 *
 * The 11az work in hardware/interfaces inserted wifi_rtt_range_request_v4 and
 * wifi_get_rtt_capabilities_v4 into the middle of wifi_hal_fn, so every slot
 * after them shifts by two relative to what libwifi-hal-mtk.so writes. The
 * platform ends up calling wifi_multi_sta_set_primary_connection where it
 * expects wifi_early_initialize, and HAL startup fails with -5.
 *
 * Let the blob fill the old layout, then repack it into the new one.
 */

#include <dlfcn.h>
#include <stddef.h>

#include <hardware_legacy/wifi_hal.h>

namespace {

constexpr char kVendorHalPath[] = "/vendor/lib64/libwifi-hal-mtk.so";

constexpr size_t kSlotV4Range = offsetof(wifi_hal_fn, wifi_rtt_range_request_v4) / sizeof(void*);
constexpr size_t kSlotV4Caps = offsetof(wifi_hal_fn, wifi_get_rtt_capabilities_v4) / sizeof(void*);
constexpr size_t kSlots = sizeof(wifi_hal_fn) / sizeof(void*);

// The repack below assumes the shift is exactly two slots. If the header gains
// or loses members this fires, so recheck the blob's layout before updating it.
static_assert(kSlots == 149, "wifi_hal_fn member count changed");

}  // namespace

extern "C" wifi_error init_wifi_vendor_hal_func_table(wifi_hal_fn* fn) {
    void** slots = reinterpret_cast<void**>(fn);

    // Stubs the caller put in every slot. The two inserted ones go back to these.
    void* stub_v4_range = slots[kSlotV4Range];
    void* stub_v4_caps = slots[kSlotV4Caps];

    void* handle = dlopen(kVendorHalPath, RTLD_NOW | RTLD_LOCAL);
    if (handle == nullptr) return WIFI_ERROR_UNKNOWN;

    auto vendor_init = reinterpret_cast<wifi_error (*)(wifi_hal_fn*)>(
            dlsym(handle, "init_wifi_vendor_hal_func_table"));
    if (vendor_init == nullptr) {
        dlclose(handle);
        return WIFI_ERROR_UNKNOWN;
    }

    // The blob writes the old layout (kSlots - 2 members), which fits in the
    // buffer the caller sized for the new one.
    wifi_error res = vendor_init(fn);
    if (res != WIFI_SUCCESS) {
        dlclose(handle);
        return res;
    }

    // Old index k to new index. Walking backwards, no slot is overwritten
    // before it is read.
    for (size_t k = kSlots - 3; k + 1 >= kSlotV4Caps; --k) slots[k + 2] = slots[k];
    for (size_t k = kSlotV4Caps - 2; k + 1 > kSlotV4Range; --k) slots[k + 1] = slots[k];

    slots[kSlotV4Caps] = stub_v4_caps;
    slots[kSlotV4Range] = stub_v4_range;

    // The handle stays open for the life of the process.
    return WIFI_SUCCESS;
}
