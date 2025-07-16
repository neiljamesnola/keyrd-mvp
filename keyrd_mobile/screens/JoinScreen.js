// KeyRD JoinScreen.js (Full Onboarding Form)
import React, { useState } from 'react';
import { ScrollView, View, Text, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';

export default function JoinScreen() {
  const [email, setEmail] = useState('');
  const [consent, setConsent] = useState('');
  const [deviceType, setDeviceType] = useState('');
  const [osVersion, setOsVersion] = useState('');

  const [age, setAge] = useState('');
  const [sex, setSex] = useState('');
  const [zipCode, setZipCode] = useState('');

  const [readinessStage, setReadinessStage] = useState('');
  const [goalType, setGoalType] = useState('');
  const [whyThisGoal, setWhyThisGoal] = useState('');
  const [nudgeStyle, setNudgeStyle] = useState('');
  const [nudgeFrequencyCap, setNudgeFrequencyCap] = useState('');
  const [quietHours, setQuietHours] = useState('');

  const [dietPattern, setDietPattern] = useState('');
  const [allergies, setAllergies] = useState(['']);
  const [medications, setMedications] = useState(['']);
  const [dailyCheckInMood, setDailyCheckInMood] = useState('');
  const [dailyCheckInEnergy, setDailyCheckInEnergy] = useState('');
  const [dailyCheckInStress, setDailyCheckInStress] = useState('');

const handleSubmit = async () => {
  const payload = {
    email,
    device_token: "", // ⚠️ Fill this in when integrating push token
    consent,
    deviceType,
    osVersion,
    age: parseInt(age) || null,
    sex,
    zip_code: zipCode,
    readiness_stage: readinessStage,
    goal_type: goalType,
    why_this_goal: whyThisGoal,
    nudge_style: nudgeStyle,
    nudge_frequency_cap: parseInt(nudgeFrequencyCap) || null,
    quiet_hours: quietHours,
    diet_type: dietPattern,
    allergies: allergies.filter((a) => a.trim() !== ""),
    medications: medications.filter((m) => m.trim() !== ""),
    mood: parseInt(dailyCheckInMood) || null,
    energy: parseInt(dailyCheckInEnergy) || null,
    stress: parseInt(dailyCheckInStress) || null,
  };

  try {
    const res = await fetch("https://your-server.com/submit_onboarding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await res.json();

    if (res.ok) {
      alert(`✅ Success! Nudge #${json.nudge_id} selected for ${json.email}`);
    } else {
      alert(`❌ Submission failed: ${json.error || "Unknown error"}`);
    }
  } catch (err) {
    alert(`🚨 Server error: ${err.message}`);
  }
};

  const handleListChange = (index, value, listSetter, list) => {
    const updated = [...list];
    updated[index] = value;
    listSetter(updated);
  };

  const addField = (listSetter, list) => {
    listSetter([...list, '']);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Join the KeyRD Beta</Text>
      <Text style={styles.subtitle}>Help us shape the future of precision nutrition. Your responses personalize your experience and power behaviorally smart nudges.</Text>

      {/* Identity Section */}
      <Text style={styles.sectionHeader}>Identity</Text>
      <Text>Email *</Text>
      <TextInput style={styles.input} value={email} onChangeText={setEmail} keyboardType="email-address" />

      <Text>Consent to Data Tracking *</Text>
      <Picker selectedValue={consent} onValueChange={setConsent} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="Yes" value="yes" />
        <Picker.Item label="No" value="no" />
      </Picker>

      <Text>Device Type *</Text>
      <Picker selectedValue={deviceType} onValueChange={setDeviceType} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="iOS" value="iOS" />
        <Picker.Item label="Android" value="Android" />
        <Picker.Item label="Wearable" value="Wearable" />
      </Picker>

      <Text>OS Version *</Text>
      <TextInput style={styles.input} value={osVersion} onChangeText={setOsVersion} />

      {/* Demographics Section */}
      <Text style={styles.sectionHeader}>Demographics</Text>
      <Text>Age *</Text>
      <TextInput style={styles.input} value={age} onChangeText={setAge} keyboardType="numeric" />

      <Text>Sex *</Text>
      <Picker selectedValue={sex} onValueChange={setSex} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="Male" value="male" />
        <Picker.Item label="Female" value="female" />
        <Picker.Item label="Nonbinary" value="nonbinary" />
        <Picker.Item label="Prefer not to say" value="prefer_not_to_say" />
      </Picker>

      <Text>Zip Code *</Text>
      <TextInput style={styles.input} value={zipCode} onChangeText={setZipCode} keyboardType="number-pad" />

      {/* Goals & Behavior */}
      <Text style={styles.sectionHeader}>Goals & Behavior</Text>
      <Text>Mindset About Health Change *</Text>
      <Picker selectedValue={readinessStage} onValueChange={setReadinessStage} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="I'm not considering change right now" value="precontemplation" />
        <Picker.Item label="I'm thinking about making a change" value="contemplation" />
        <Picker.Item label="I'm planning to start soon" value="preparation" />
        <Picker.Item label="I've recently started" value="action" />
        <Picker.Item label="I've been maintaining for a while" value="maintenance" />
      </Picker>

      <Text>Primary Health Goal *</Text>
      <Picker selectedValue={goalType} onValueChange={setGoalType} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="Weight Loss" value="weight_loss" />
        <Picker.Item label="Improve Labs" value="better_labs" />
        <Picker.Item label="Lower Blood Pressure" value="lower_bp" />
        <Picker.Item label="Increase Energy" value="energy" />
        <Picker.Item label="Improve Mood" value="mood" />
      </Picker>

      <Text>Why is this goal important to you? *</Text>
      <TextInput style={styles.input} value={whyThisGoal} onChangeText={setWhyThisGoal} placeholder="e.g., Reduce meds, feel better" />

      <Text>Preferred Nudge Style *</Text>
      <Picker selectedValue={nudgeStyle} onValueChange={setNudgeStyle} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="Gentle" value="gentle" />
        <Picker.Item label="Motivating" value="motivating" />
        <Picker.Item label="Directive" value="directive" />
        <Picker.Item label="Humorous" value="humorous" />
      </Picker>

      <Text>Max Nudges per Day (1–5) *</Text>
      <TextInput style={styles.input} value={nudgeFrequencyCap} onChangeText={setNudgeFrequencyCap} keyboardType="numeric" />

      <Text>Quiet Hours (e.g., 21:00–07:00) *</Text>
      <TextInput style={styles.input} value={quietHours} onChangeText={setQuietHours} />

      {/* Dietary & Clinical */}
      <Text style={styles.sectionHeader}>Dietary & Clinical</Text>

      <Text>General Diet Pattern</Text>
      <Picker selectedValue={dietPattern} onValueChange={setDietPattern} style={styles.picker}>
        <Picker.Item label="Select..." value="" />
        <Picker.Item label="Omnivore" value="omnivore" />
        <Picker.Item label="Vegetarian" value="vegetarian" />
        <Picker.Item label="Vegan" value="vegan" />
        <Picker.Item label="Pescatarian" value="pescatarian" />
        <Picker.Item label="Keto" value="keto" />
      </Picker>

      <Text>Allergies</Text>
      {allergies.map((item, i) => (
        <TextInput
          key={i}
          style={styles.input}
          placeholder={`Allergy ${i + 1}`}
          value={item}
          onChangeText={(val) => handleListChange(i, val, setAllergies, allergies)}
        />
      ))}
      <Button title="Add Allergy" onPress={() => addField(setAllergies, allergies)} />

      <Text>Medications</Text>
      {medications.map((item, i) => (
        <TextInput
          key={i}
          style={styles.input}
          placeholder={`Medication ${i + 1}`}
          value={item}
          onChangeText={(val) => handleListChange(i, val, setMedications, medications)}
        />
      ))}
      <Button title="Add Medication" onPress={() => addField(setMedications, medications)} />

      <Text style={styles.sectionHeader}>Daily Check-In (Typical)</Text>

      <Text>Mood (1–5)</Text>
      <TextInput style={styles.input} value={dailyCheckInMood} onChangeText={setDailyCheckInMood} keyboardType="numeric" />

      <Text>Energy (1–5)</Text>
      <TextInput style={styles.input} value={dailyCheckInEnergy} onChangeText={setDailyCheckInEnergy} keyboardType="numeric" />

      <Text>Stress (1–5)</Text>
      <TextInput style={styles.input} value={dailyCheckInStress} onChangeText={setDailyCheckInStress} keyboardType="numeric" />

      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Submit</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    paddingBottom: 60
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 10
  },
  subtitle: {
    fontSize: 14,
    color: '#555',
    textAlign: 'center',
    marginBottom: 30
  },
  sectionHeader: {
    fontSize: 18,
    fontWeight: '600',
    marginTop: 20,
    marginBottom: 10
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 6,
    marginBottom: 15
  },
  picker: {
    borderWidth: 1,
    borderColor: '#ccc',
    marginBottom: 15
  },
  button: {
    backgroundColor: '#003f8a',
    padding: 14,
    borderRadius: 30,
    alignItems: 'center',
    marginTop: 30
  },
  buttonText: {
    color: 'white',
    fontWeight: '600'
  }
});
