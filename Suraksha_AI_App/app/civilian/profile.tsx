import React from 'react';
import { View, Text, StyleSheet, ScrollView, Switch, TouchableOpacity, TextInput } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Header } from '../../src/components/common/Header';
import { ConnectionStatus } from '../../src/components/common/ConnectionStatus';
import { Shield, PhoneCall, HeartPulse, WifiOff, Globe, Plus, AlertCircle } from 'lucide-react-native';
import { useUserStore } from '../../src/store/useUserStore';
import { colors, typography, spacing, radius, shadows } from '../../src/theme';

import { useTranslation, LanguageCode } from '../../src/i18n';

export default function ProfileScreen() {
  const { profile, toggleOfflineMode } = useUserStore();
  const { t, language, changeLanguage } = useTranslation();

  return (
    <SafeAreaView style={styles.container}>
      <Header title={t('emergencyProfile')} />
      <ConnectionStatus />

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Offline Emergency Mode Switcher */}
        <View style={styles.card}>
          <View style={styles.rowBetween}>
            <View style={styles.rowLeft}>
              <View style={[styles.iconBox, { backgroundColor: 'rgba(239, 68, 68, 0.15)' }]}>
                <WifiOff size={18} color={colors.status.error} />
              </View>
              <View>
                <Text style={styles.cardTitle}>{t('offlineEmergencyMode')}</Text>
                <Text style={styles.cardSubtitle}>{t('offlineModeDesc')}</Text>
              </View>
            </View>
            <Switch
              value={profile.offlineModeEnabled}
              onValueChange={toggleOfflineMode}
              trackColor={{ false: colors.border.default, true: colors.severity.CRITICAL.main }}
              thumbColor="#FFF"
            />
          </View>
        </View>

        {/* Medical Information */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <HeartPulse size={18} color={colors.severity.CRITICAL.text} />
            <Text style={styles.cardTitle}>{t('civilianMedicalInfo')}</Text>
          </View>
          <View style={styles.infoGrid}>
            <View style={styles.infoBox}>
              <Text style={styles.infoLabel}>{t('bloodGroup')}</Text>
              <Text style={styles.infoValue}>{profile.bloodGroup}</Text>
            </View>
            <View style={styles.infoBox}>
              <Text style={styles.infoLabel}>{t('medicalConditions')}</Text>
              <Text style={styles.infoValue}>{profile.medicalConditions}</Text>
            </View>
          </View>
        </View>

        {/* Emergency Contacts List */}
        <View style={styles.card}>
          <View style={styles.rowBetween}>
            <View style={styles.cardHeader}>
              <PhoneCall size={18} color={colors.primary.main} />
              <Text style={styles.cardTitle}>{t('emergencyHotlinesContacts')}</Text>
            </View>
          </View>

          {profile.emergencyContacts.map((contact) => (
            <View key={contact.id} style={styles.contactRow}>
              <View>
                <Text style={styles.contactName}>
                  {contact.name} {contact.isPrimary && `(${t('primarySos')})`}
                </Text>
                <Text style={styles.contactRel}>{contact.relation}</Text>
              </View>
              <TouchableOpacity style={styles.callChip} activeOpacity={0.7}>
                <PhoneCall size={12} color="#FFF" />
                <Text style={styles.callNumber}>{contact.phoneNumber}</Text>
              </TouchableOpacity>
            </View>
          ))}
        </View>

        {/* Language Selection */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Globe size={18} color={colors.safety.main} />
            <Text style={styles.cardTitle}>{t('preferredLanguage')}</Text>
          </View>
          <View style={styles.langRow}>
            {[
              { code: 'EN', label: 'English' },
              { code: 'HI', label: 'हिंदी (Hindi)' },
              { code: 'GU', label: 'ગુજરાતી (Gujarati)' },
            ].map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[
                  styles.langChip,
                  language === lang.code && styles.langChipActive,
                ]}
                onPress={() => changeLanguage(lang.code as LanguageCode)}
                accessibilityRole="button"
                accessibilityLabel={`${lang.label}${language === lang.code ? ', selected' : ''}`}
              >
                <Text
                  style={[
                    styles.langText,
                    language === lang.code && styles.langTextActive,
                  ]}
                >
                  {lang.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
  },
  content: {
    flex: 1,
    padding: spacing.md,
  },
  card: {
    backgroundColor: colors.background.secondary,
    borderRadius: radius.lg,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border.subtle,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
  cardTitle: {
    color: colors.text.primary,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.heavy,
    letterSpacing: 0.5,
  },
  cardSubtitle: {
    color: colors.text.secondary,
    fontSize: 11,
  },
  rowBetween: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  rowLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    flex: 1,
  },
  iconBox: {
    width: 34,
    height: 34,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  infoGrid: {
    gap: spacing.sm,
  },
  infoBox: {
    backgroundColor: colors.background.tertiary,
    padding: spacing.sm,
    borderRadius: radius.md,
  },
  infoLabel: {
    color: colors.text.secondary,
    fontSize: 10,
    fontWeight: typography.fontWeight.semibold,
  },
  infoValue: {
    color: colors.text.primary,
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.bold,
    marginTop: 2,
  },
  contactRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: spacing.xs,
    borderBottomWidth: 1,
    borderBottomColor: colors.border.subtle,
  },
  contactName: {
    color: colors.text.primary,
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.bold,
  },
  contactRel: {
    color: colors.text.secondary,
    fontSize: 11,
  },
  callChip: {
    backgroundColor: colors.primary.main,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: radius.full,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  callNumber: {
    color: '#FFF',
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  langRow: {
    flexDirection: 'row',
    gap: spacing.xs,
  },
  langChip: {
    flex: 1,
    backgroundColor: colors.background.tertiary,
    paddingVertical: spacing.xs,
    borderRadius: radius.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.border.subtle,
  },
  langChipActive: {
    backgroundColor: colors.safety.main,
    borderColor: colors.safety.light,
  },
  langText: {
    color: colors.text.secondary,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.semibold,
  },
  langTextActive: {
    color: '#FFF',
    fontWeight: typography.fontWeight.bold,
  },
});
