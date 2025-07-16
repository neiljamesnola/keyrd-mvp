// app/(tabs)/register.tsx

import React, { useEffect, useState } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

export default function Register() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const pushToken = await registerForPushNotificationsAsync();
      setToken(pushToken);
    })();
  }, []);

  async function registerForPushNotificationsAsync(): Promise<string | null> {
    if (!Device.isDevice) {
      Alert.alert('Error', 'Must use a physical device for push notifications.');
      return null;
    }

    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      Alert.alert('Permission denied', 'Failed to get push token.');
      return null;
    }

    const { data } = await Notifications.getExpoPushTokenAsync();
    return data;
  }

  async function sendTokenToBackend() {
    if (!token) {
      Alert.alert('Token not ready', 'Wait until the token is generated.');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/onboarding', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'test@example.com',
          device_token: token,
        }),
      });

      const json = await response.json();
      Alert.alert('Success', JSON.stringify(json));
    } catch (error) {
      console.error('Failed to register device token:', error);
      Alert.alert('Error', 'Could not connect to backend.');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Push Token</Text>
      <Text selectable style={styles.token}>
        {token || 'Generating...'}
      </Text>
      <Button title="Send to Backend" onPress={sendTokenToBackend} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 10,
    fontSize: 16,
  },
  token: {
    marginBottom: 20,
    color: 'gray',
  },
});
