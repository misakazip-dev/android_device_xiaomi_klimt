/*
 * SPDX-FileCopyrightText: WitAqua
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package miui.telephony;

import android.app.AppGlobals;
import android.content.Context;

public class SubscriptionManagerEx {
    private static final SubscriptionManagerEx sInstance = new SubscriptionManagerEx();

    public static SubscriptionManagerEx getDefault() {
        return sInstance;
    }

    public int setDisplayNameForSubscription(String displayName, int subId) {
        Context context = AppGlobals.getInitialApplication();
        if (context == null) {
            return 0;
        }
        android.telephony.SubscriptionManager subscriptionManager =
                context.getSystemService(android.telephony.SubscriptionManager.class);
        if (subscriptionManager == null) {
            return 0;
        }
        return subscriptionManager.setDisplayName(displayName, subId,
                android.telephony.SubscriptionManager.NAME_SOURCE_USER_INPUT);
    }

    protected SubscriptionManagerEx() {}
}
