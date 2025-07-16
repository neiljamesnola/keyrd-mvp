// keyrd_mobile/screens/DashboardScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet, Alert } from 'react-native';

export default function DashboardScreen({ expoPushToken }) {
  const [goalText, setGoalText] = useState('');
  const [nudgeText, setNudgeText] = useState('');
  const [nudges, setNudges] = useState([]);

  const handleAddNudge = async () => {
    if (!goalText || !nudgeText) return;

    const newNudge = {
      id: Date.now().toString(),
      goal: goalText,
      nudge: nudgeText,
    };

    // Update UI locally
    setNudges(prev => [...prev, newNudge]);
    setGoalText('');
    setNudgeText('');

    // Send to backend
    try {
      const response = await fetch('http://localhost:5000/log_nudge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 1, // TODO: Replace with dynamic user ID
          goal: newNudge.goal,
          nudge: newNudge.nudge,
          push_token: expoPushToken,
        }),
      });

      const data = await response.json();
      console.log('✅ Nudge saved:', data);
    } catch (err) {
      console.error('❌ Error sending nudge:', err);
      Alert.alert('Error', 'Failed to send nudge to backend');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>📊 KeyRD Dashboard</Text>

      <TextInput
        style={styles.input}
        placeholder="Enter your goal (e.g., walk 10,000 steps)"
        value={goalText}
        onChangeText={setGoalText}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter your nudge message"
        value={nudgeText}
        onChangeText={setNudgeText}
      />
      <Button title="Save Nudge" onPress={handleAddNudge} />

      <FlatList
        data={nudges}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.goal}>🎯 Goal: {item.goal}</Text>
            <Text style={styles.nudge}>💡 Nudge: {item.nudge}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  heading: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  input: {
    borderWidth: 1, borderColor: '#ccc', borderRadius: 8,
    padding: 10, marginBottom: 10
  },
  card: {
    padding: 15, marginVertical: 8, borderWidth: 1,
    borderRadius: 10, borderColor: '#ddd', backgroundColor: '#f9f9f9'
  },
  goal: { fontWeight: 'bold', fontSize: 16 },
  nudge: { marginTop: 5, color: '#555' }
});
