// KeyRD HomeScreen.js
import React from 'react';
import { View, Text, Image, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function HomeScreen() {
  const navigation = useNavigation();

  return (
    <ScrollView className="flex-1 bg-white">

      {/* Header */}
      <View className="items-center py-6 border-b border-gray-200">
        <Image source={require('../assets/logo.png')} style={{ height: 80, resizeMode: 'contain' }} />
      </View>

      {/* Hero Section */}
      <View className="items-center px-6 py-8">
        <Image source={require('../assets/hero-illustration.png')} style={{ width: 240, height: 240, resizeMode: 'contain', marginBottom: 16 }} />
        <Text className="text-2xl font-bold text-center mb-2">Welcome to KeyRD</Text>
        <Text className="text-base text-gray-600 text-center mb-4 px-2">
          Now in beta. Help us shape the future of digital nutrition—rooted in evidence, optimized for you.
        </Text>
        <TouchableOpacity
          className="bg-[#003f8a] px-6 py-3 rounded-full"
          onPress={() => navigation.navigate('Join')}
        >
          <Text className="text-white font-semibold text-base text-center">Join the Beta</Text>
        </TouchableOpacity>
      </View>

      {/* How It Works */}
      <View className="px-6 py-8 bg-white">
        <Text className="text-xl font-semibold text-center mb-6">How It Works</Text>
        <View className="space-y-10">
          <View className="items-center">
            <Image source={require('../assets/onboarding.png')} style={{ width: 64, height: 64, marginBottom: 8 }} />
            <Text className="text-lg font-semibold mb-1">Complete onboarding</Text>
            <Text className="text-sm text-gray-600 text-center">
              Provide information about your health, preferences, and lifestyle.
            </Text>
          </View>
          <View className="items-center">
            <Image source={require('../assets/nudges.png')} style={{ width: 64, height: 64, marginBottom: 8 }} />
            <Text className="text-lg font-semibold mb-1">Receive real-time nudges</Text>
            <Text className="text-sm text-gray-600 text-center">
              Get gentle reminders and actionable advice tailored to you.
            </Text>
          </View>
          <View className="items-center">
            <Image source={require('../assets/progress.png')} style={{ width: 64, height: 64, marginBottom: 8 }} />
            <Text className="text-lg font-semibold mb-1">Track your progress</Text>
            <Text className="text-sm text-gray-600 text-center">
              Monitor your journey with insight-fueled feedback and analytics.
            </Text>
          </View>
        </View>
      </View>

      {/* Your Data, Empowered */}
      <View className="bg-[#f4f8fb] px-6 py-12">
        <View className="items-center">
          <Image source={require('../assets/data-powered.png')} style={{ width: 320, height: 200, resizeMode: 'contain', marginBottom: 16 }} />
          <Text className="text-xl font-semibold mb-2 text-center">Your Data, Empowered</Text>
          <Text className="text-sm text-gray-700 text-center mb-2">
            Your insights remain private, protected, and used only to support your success.
          </Text>
          <Text className="text-sm text-gray-700 text-center">
            We don’t sell your data. We use it only to help you thrive—with purpose, clarity, and trust.
          </Text>
        </View>
      </View>

      {/* Footer */}
      <View className="bg-gray-100 px-4 py-6 border-t border-gray-200">
        <Text className="text-center text-xs text-gray-500">
          © 2025 KeyRD. Privacy-respecting, science-based, user-powered.
        </Text>
      </View>

    </ScrollView>
  );
}
