import * as Notifications from 'expo-notifications';
import Constants from 'expo-constants';
import { Alert, Platform } from 'react-native';

const BACKEND_URL = 'http://localhost:5000'; // Replace with production URL when deploying

export async function registerForPushNotificationsAsync() {
  if (!Constants.isDevice) {
    Alert.alert('Push notifications require a physical device');
    return null;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    Alert.alert('Permission denied for push notifications');
    return null;
  }

  try {
    const { data: token } = await Notifications.getExpoPushTokenAsync({
      // Adjust experienceId only if using Expo Go. Omit if using EAS builds.
      projectId: Constants.expoConfig?.extra?.eas?.projectId,
    });
    return token;
  } catch (err) {
    console.error('❌ Failed to get Expo push token:', err);
    return null;
  }
}

export async function registerDeviceToken(userId, token) {
  try {
    const response = await fetch(`${BACKEND_URL}/push/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, device_token: token }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Device token registered with backend:', data);
    return data;
  } catch (err) {
    console.error('❌ Error registering device token with backend:', err);
    return null;
  }
}
