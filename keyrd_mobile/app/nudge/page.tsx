// File: app/nudge/page.tsx

'use client';

import React, { useEffect, useState } from 'react';
import { Text, View, ActivityIndicator, StyleSheet } from 'react-native';
import { selectAndSendNudge } from '@/utils/push';

export default function NudgePage() {
  const [nudge, setNudge] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNudge = async () => {
      try {
        const result = await selectAndSendNudge('user123'); // Use real user ID in production
        setNudge(result);
      } catch (err) {
        console.error('[NudgePage] Failed to fetch nudge:', err);
        setError('Something went wrong while selecting a nudge.');
      }
    };

    fetchNudge();
  }, []);

  return (
    <View style={styles.container}>
      {error ? (
        <Text style={styles.error}>{error}</Text>
      ) : nudge ? (
        <Text style={styles.nudge}>🤖 Nudge: {nudge}</Text>
      ) : (
        <ActivityIndicator size="large" color="#007AFF" />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  nudge: {
    fontSize: 24,
    textAlign: 'center',
    color: '#333',
  },
  error: {
    color: 'red',
    fontSize: 18,
    textAlign: 'center',
  },
});
