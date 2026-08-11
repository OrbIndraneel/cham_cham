import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function SOSScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🆘 Emergency SOS & Broadcast</Text>
      <TouchableOpacity style={styles.sosButton}>
        <Text style={styles.sosText}>SEND SOS</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0F172A' },
  title: { fontSize: 22, fontWeight: 'bold', color: '#F8FAFC', marginBottom: 30 },
  sosButton: { width: 180, height: 180, borderRadius: 90, backgroundColor: '#DC2626', justifyContent: 'center', alignItems: 'center', elevation: 10 },
  sosText: { fontSize: 24, fontWeight: 'bold', color: '#FFFFFF' }
});
