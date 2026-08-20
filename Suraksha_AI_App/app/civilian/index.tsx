import React from 'react';
import { View, StyleSheet, StatusBar, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import { HazardMap } from '../../src/components/map/HazardMap';
import { MapFloatingControls } from '../../src/components/map/MapFloatingControls';
import { FloatingAlertCard } from '../../src/components/civilian/FloatingAlertCard';
import { SafeguardBottomSheet } from '../../src/components/civilian/SafeguardBottomSheet';

export default function CivilianHomeScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const handleSosPress = () => {
    router.push('/modal/sos' as any);
  };

  const handleNavigationPress = () => {
    router.push('/civilian/evacuation' as any);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="transparent" translucent />

      {/* FULL-SCREEN IMMERSIVE MAP */}
      <View style={styles.mapArea}>
        <HazardMap />

        {/* Floating Circular Controls on Top Left */}
        <View style={[styles.controlsPosition, { top: Math.max(insets.top + 70, 75) }]}>
          <MapFloatingControls />
        </View>

        {/* Floating Critical Alert Banner near Top Center */}
        <View
          style={[
            styles.alertBannerOverlay,
            { top: Math.max(insets.top + 8, 16) },
          ]}
          pointerEvents="box-none"
        >
          <FloatingAlertCard
            title="CRITICAL ALERT: Secondary Landslide Risk"
            subtitle="Detected in Zone B."
            actionText="Rerouting active evacuation path..."
          />
        </View>

        {/* Translucent Dark Bottom Sheet */}
        <View style={styles.bottomSheetPosition} pointerEvents="box-none">
          <SafeguardBottomSheet
            onSosPress={handleSosPress}
            onNavigationPress={handleNavigationPress}
          />
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0A0F1A',
  },
  mapArea: {
    flex: 1,
    position: 'relative',
  },
  controlsPosition: {
    position: 'absolute',
    left: 0,
    zIndex: 20,
  },
  alertBannerOverlay: {
    position: 'absolute',
    left: 14,
    right: 14,
    zIndex: 10,
  },
  bottomSheetPosition: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 30,
  },
});

