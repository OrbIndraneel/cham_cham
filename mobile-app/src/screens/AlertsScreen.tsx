import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function AlertsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🚨 Early Warning Alerts</Text>
      <Text style={styles.subtitle}>Real-time notifications pushed by GNN Cascade Model</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0F172A' },
  title: { fontSize: 20, fontWeight: 'bold', color: '#EF4444', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#94A3B8', textAlign: 'center', paddingHorizontal: 20 },
});
