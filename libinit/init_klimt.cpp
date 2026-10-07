// SPDX-FileCopyrightText: WitAqua
// SPDX-FileCopyrightText: The LineageOS Project
// SPDX-License-Identifier: Apache-2.0

#include <cstring>

#include <android-base/logging.h>
#include <android-base/properties.h>
#include <sys/system_properties.h>

#include "vendor_init.h"

namespace {

void override_property(const char* name, const char* value) {
    auto* property = const_cast<prop_info*>(__system_property_find(name));
    int result = property
            ? __system_property_update(property, value, std::strlen(value))
            : __system_property_add(name, std::strlen(name), value, std::strlen(value));
    if (result != 0) {
        LOG(ERROR) << "Unable to set " << name;
    }
}

}  // namespace

void vendor_load_properties() {
    // Match the SKU files in stock /odm/etc. TW and ID use the global IDs.
    const auto hwc = android::base::GetProperty("ro.boot.hwc", "");
    // SystemConfig loads vendor/etc/permissions/sku_<vendor SKU> at boot.
    // Derive this selector from the same hardware region used for FeliCa.
    override_property("ro.boot.product.vendor.sku", hwc == "JP" ? "klimt_jp" : "klimt");

    const char* product = "klimt_global";
    const char* model = "2506BPN68G";
    if (hwc == "JP") {
        product = "klimt_jp";
        model = "2506BPN68R";
    } else if (hwc == "EEA") {
        product = "klimt_eea";
    } else if (hwc == "RU") {
        product = "klimt_ru";
    } else if (hwc == "TR") {
        product = "klimt_tr";
    }

    // Mobile FeliCa sends Build.MODEL to its server. Publish the hardware model
    // before init derives product properties and before zygote starts.
    override_property("ro.product.model", model);

    // Derive ro.product.name from the build's partition properties. The build
    // description and vendor-style fingerprint use klimt_global. Keep
    // SKU-specific product IDs for attestation.

    // These IDs must match the values provisioned in the TEE for this SKU.
    override_property("ro.product.model_for_attestation", model);
    override_property("ro.product.name_for_attestation", product);
    override_property("ro.product.brand_for_attestation", "Xiaomi");
}
