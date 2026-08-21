import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Shield, UserCheck, Radio, AlertOctagon, Sparkles, MapPin } from 'lucide-react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, typography, spacing, radius, shadows } from '../src/theme';
import { useUserStore } from '../src/store/useUserStore';

export default function HomeScreen() {
  const router = useRouter();
  const { setRole } = useUserStore();

  const handleSelectRole = (role: 'CIVILIAN' | 'AUTHORITY') => {
    setRole(role);
    if (role === 'CIVILIAN') {
      router.replace('/civilian' as any);
    } else {
      router.replace('/authority' as any);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Top App Header */}
      <View style={styles.header}>
        <View style={styles.logoBox}>
          <Shield size={32} color={colors.primary.main} />
        </View>
        <Text style={styles.title}>SURAKSHA AI</Text>
        <Text style={styles.subtitle}>
          AI-Powered Disaster Management & Safe Evacuation Platform
        </Text>
        <View style={styles.badgeRow}>
          <View style={styles.sihBadge}>
            <Sparkles size={12} color={colors.safety.main} />
            <Text style={styles.sihText}>SIH 2026 Emergency AI Engine</Text>
          </View>
        </View>
      </View>

      {/* Role Selection Options */}
      <View style={styles.roleSelectionContainer}>
        <Text style={styles.sectionTitle}>SELECT ACCESS PORTAL</Text>

        {/* Civilian Role Card */}
        <TouchableOpacity
          style={styles.roleCard}
          onPress={() => handleSelectRole('CIVILIAN')}
          activeOpacity={0.8}
        >
          <View style={[styles.roleIconBox, { backgroundColor: 'rgba(59, 130, 246, 0.15)' }]}>
            <UserCheck size={28} color={colors.primary.main} />
          </View>
          <View style={styles.roleTextContainer}>
            <Text style={styles.roleTitle}>CIVILIAN / EVACUEE PORTAL</Text>
            <Text style={styles.roleDesc}>
              Dynamic safe evacuation routes, live hazard map, shelter capacity tracking & 1-tap SOS emergency dispatch.
            </Text>
            <View style={styles.tagRow}>
              <Text style={styles.tagText}>• Live GIS Map</Text>
              <Text style={styles.tagText}>• Dynamic Safest Path</Text>
              <Text style={styles.tagText}>• Offline Mode</Text>
            </View>
          </View>
        </TouchableOpacity>

        {/* Authority Role Card */}
        <TouchableOpacity
          style={[styles.roleCard, styles.authorityCard]}
          onPress={() => handleSelectRole('AUTHORITY')}
          activeOpacity={0.8}
        >
          <View style={[styles.roleIconBox, { backgroundColor: 'rgba(249, 115, 22, 0.15)' }]}>
            <Radio size={28} color={colors.safety.main} />
          </View>
          <View style={styles.roleTextContainer}>
            <Text style={[styles.roleTitle, { color: colors.safety.main }]}>
              AUTHORITY / CONTROL ROOM
            </Text>
            <Text style={styles.roleDesc}>
              Disaster dashboard, AI rainfall & surge scenario simulator, secondary cascade predictor & emergency alert dispatch.
            </Text>
            <View style={styles.tagRow}>
              <Text style={[styles.tagText, { color: colors.safety.light }]}>• AI Cascade Simulator</Text>
              <Text style={[styles.tagText, { color: colors.safety.light }]}>• Alert Dispatch</Text>
            </View>
          </View>
        </TouchableOpacity>
      </View>

      {/* Demo Active Disaster Region Notice */}
      <View style={styles.demoFooter}>
        <MapPin size={14} color={colors.text.secondary} />
        <Text style={styles.demoText}>
          Active Demo Region: <Text style={{ color: colors.text.primary, fontWeight: 'bold' }}>Vadodara, Gujarat (Vishwamitri Flood)</Text>
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
    paddingHorizontal: spacing.lg,
    justifyContent: 'space-between',
    paddingVertical: spacing.md,
  },
  header: {
    alignItems: 'center',
    marginTop: spacing.lg,
  },
  logoBox: {
    width: 64,
    height: 64,
    borderRadius: radius.xl,
    backgroundColor: 'rgba(59, 130, 246, 0.15)',
    borderWidth: 2,
    borderColor: colors.border.strong,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
    ...shadows.glowBlue,
  },
  title: {
    color: colors.text.primary,
    fontSize: typography.fontSize.display,
    fontWeight: typography.fontWeight.heavy,
    letterSpacing: 1.5,
  },
  subtitle: {
    color: colors.text.secondary,
    fontSize: typography.fontSize.sm,
    textAlign: 'center',
    marginTop: spacing.xs,
    paddingHorizontal: spacing.md,
  },
  badgeRow: {
    marginTop: spacing.md,
  },
  sihBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(249, 115, 22, 0.15)',
    paddingHorizontal: spacing.md,
    paddingVertical: 4,
    borderRadius: radius.full,
    borderWidth: 1,
    borderColor: 'rgba(249, 115, 22, 0.4)',
    gap: 6,
  },
  sihText: {
    color: colors.safety.main,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  roleSelectionContainer: {
    gap: spacing.md,
  },
  sectionTitle: {
    color: colors.text.secondary,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.heavy,
    letterSpacing: 1,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  roleCard: {
    flexDirection: 'row',
    backgroundColor: colors.background.secondary,
    borderRadius: radius.xl,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border.strong,
    gap: spacing.md,
    ...shadows.md,
  },
  authorityCard: {
    borderColor: 'rgba(249, 115, 22, 0.4)',
  },
  roleIconBox: {
    width: 48,
    height: 48,
    borderRadius: radius.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  roleTextContainer: {
    flex: 1,
  },
  roleTitle: {
    color: colors.primary.light,
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.heavy,
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  roleDesc: {
    color: colors.text.secondary,
    fontSize: typography.fontSize.xs,
    lineHeight: 18,
    marginBottom: spacing.xs,
  },
  tagRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    flexWrap: 'wrap',
  },
  tagText: {
    color: colors.primary.main,
    fontSize: 10,
    fontWeight: typography.fontWeight.bold,
  },
  demoFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.background.secondary,
    paddingVertical: spacing.sm,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border.subtle,
    gap: 6,
  },
  demoText: {
    color: colors.text.secondary,
    fontSize: typography.fontSize.xs,
  },
});
