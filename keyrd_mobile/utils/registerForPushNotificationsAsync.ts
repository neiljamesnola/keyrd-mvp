// app/utils/registerForPushNotificationsAsync.ts

import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

/**
 * Registers the device for push notifications and returns the Expo push token.
 * Must be called from a physical device.
 */
export async function registerForPushNotificationsAsync(): Promise<string | undefined> {
  try {
    // Ensure we're on a physical device
    if (!Device.isDevice) {
      console.warn('❌ Push notifications require a physical device.');
      return;
    }

    // Get existing permissions
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    // Request permissions if not already granted
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      console.warn('❌ Push notification permissions denied.');
      return;
    }

    // Get Expo push token
    const { data: token } = await Notifications.getExpoPushTokenAsync();
    console.log('✅ Expo Push Token:', token);

    // Set Android-specific notification channel
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }

    return token;
  } catch (error) {
    console.error('🚨 Error registering for push notifications:', error);
    return;
  }
}
