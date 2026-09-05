/*
 * SPDX-FileCopyrightText: WitAqua
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package miui.util;

import android.os.SystemProperties;

/**
 * MIUI reads device features from /system/etc/device_features/<device>.xml. Nothing
 * on this build ships those files.
 */
public class FeatureParser {
    public static String getString(String key) {
        if ("vendor".equals(key)) {
            return SystemProperties.get("ro.hardware", "").startsWith("mt")
                    || SystemProperties.get("ro.board.platform", "").startsWith("mt")
                    ? "mediatek"
                    : null;
        }
        return null;
    }

    public static Boolean getBoolean(String key, boolean defaultValue) {
        return defaultValue;
    }

    public static Integer getInteger(String key, int defaultValue) {
        return defaultValue;
    }

    public static String[] getStringArray(String key) {
        return null;
    }

    public static int[] getIntArray(String key) {
        return null;
    }

    private FeatureParser() {}
}
