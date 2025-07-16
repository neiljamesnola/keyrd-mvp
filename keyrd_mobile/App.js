import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, View, Platform } from 'react-native';
import * as Notifications from 'expo-notifications';
import { registerForPushNotificationsAsync, registerDeviceToken } from './utils/push';

// Notification handler configuration
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

export default function App() {
  const [expoPushToken, setExpoPushToken] = useState(null);
  const notificationListener = useRef(null);
  const responseListener = useRef(null);

  useEffect(() => {
    let isMounted = true;

    // Register and save the push token
    const initializePush = async () => {
      const token = await registerForPushNotificationsAsync();
      if (token && isMounted) {
        console.log('📲 Expo Push Token:', token);
        setExpoPushToken(token);
        await registerDeviceToken(1, token); // TODO: replace with dynamic user ID
      }
    };

    initializePush();

    // Listen for incoming notifications
    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      console.log('🔔 Notification received:', notification);
    });

    // Listen for user interaction with notifications
    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      console.log('📬 Notification response received:', response);
    });

    return () => {
      isMounted = false;
      if (notificationListener.current) {
        Notifications.removeNotificationSubscription(notificationListener.current);
      }
      if (responseListener.current) {
        Notifications.removeNotificationSubscription(responseListener.current);
      }
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>KeyRD iOS Push Notification Ready 🚀</Text>
      {expoPushToken && (
        <Text selectable style={styles.token}>
          {expoPushToken}
        </Text>
      )}
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    textAlign: 'center',
  },
  token: {
    marginTop: 10,
    fontSize: 12,
    color: '#555',
    fontFamily: Platform.select({ ios: 'Courier', android: 'monospace' }),
  },
});
