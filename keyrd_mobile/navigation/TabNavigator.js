import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import DashboardScreen from '../screens/DashboardScreen';
import ProfileScreen from '../screens/ProfileScreen';
import SettingsScreen from '../screens/SettingsScreen';
import AboutScreen from '../screens/AboutScreen';
import JoinScreen from '../screens/JoinScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs({ expoPushToken }) {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Dashboard"
        options={{ title: '🏠 Dashboard' }}
        children={() => <DashboardScreen expoPushToken={expoPushToken} />}
      />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
      <Tab.Screen name="About" component={AboutScreen} />
    </Tab.Navigator>
  );
}

export default function TabNavigator({ expoPushToken }) {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Main" children={() => <MainTabs expoPushToken={expoPushToken} />} />
      <Stack.Screen name="Join" component={JoinScreen} />
    </Stack.Navigator>
  );
}
