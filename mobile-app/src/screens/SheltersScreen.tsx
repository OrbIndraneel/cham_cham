import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function SheltersScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🏫 Safe Emergency Shelters</Text>
      <Text style={styles.subtitle}>Nearby shelters with real-time capacity & routing</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0F172A' },
  title: { fontSize: 20, fontWeight: 'bold', color: '#10B981', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#94A3B8', textAlign: 'center', paddingHorizontal: 20 },
});
