/*
 * SPDX-FileCopyrightText: WitAqua
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package miui.util;

import android.content.Context;
import android.net.Uri;
import android.os.VibrationAttributes;

/**
 * MIUI's linear motor haptics. Only miuix's HapticFeedbackCompat calls this, and it
 * treats an unsupported motor as "fall back to the platform's own haptics", so every
 * capability query answers no and every playback request is a no-op.
 */
public class HapticFeedbackUtil {
    public HapticFeedbackUtil(Context context, boolean useSystemVibrator) {}

    public static boolean isSupportLinearMotorVibrate() {
        return false;
    }

    public static boolean isSupportLinearMotorVibrate(int effectId) {
        return false;
    }

    public boolean isSupportExtHapticFeedback(int effectId) {
        return false;
    }

    public boolean performExtHapticFeedback(int effectId) {
        return false;
    }

    public boolean performExtHapticFeedback(int effectId, boolean always) {
        return false;
    }

    public boolean performExtHapticFeedback(int effectId, int repeat) {
        return false;
    }

    public boolean performExtHapticFeedback(int effectId, int repeat, boolean always) {
        return false;
    }

    public boolean performExtHapticFeedback(int effectId, double amplitude, String reason) {
        return false;
    }

    public boolean performExtHapticFeedback(Uri uri) {
        return false;
    }

    public boolean performExtHapticFeedback(Uri uri, boolean always) {
        return false;
    }

    public boolean performExtHapticFeedback(VibrationAttributes attributes, int effectId) {
        return false;
    }

    public boolean performExtHapticFeedback(VibrationAttributes attributes, int effectId,
            boolean always) {
        return false;
    }

    public boolean performHapticFeedback(int effectId, boolean always) {
        return false;
    }

    public boolean performHapticFeedback(int effectId, boolean always, int flags) {
        return false;
    }

    public boolean performHapticFeedback(int effectId, double amplitude, String reason) {
        return false;
    }

    public boolean performHapticFeedback(VibrationAttributes attributes, int effectId,
            boolean always) {
        return false;
    }

    public boolean performHapticFeedback(VibrationAttributes attributes, int effectId,
            boolean always, int flags) {
        return false;
    }

    public boolean performHapticFeedback(VibrationAttributes attributes, int effectId,
            double amplitude, String reason) {
        return false;
    }

    public void stop() {}

    public void release() {}
}
