import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react-native';
import { colors, radius, spacing, typography } from '../../theme';
import { useOfflineStore } from '../../store/useOfflineStore';

export const ConnectionStatus: React.FC = () => {
  const { isOnline, isSyncing, setOnlineState, triggerSync } = useOfflineStore();

  const handleToggleOnline = async () => {
    if (!isOnline) {
      // Switching from Offline to Online -> Trigger Sync Simulation
      await triggerSync();
    } else {
      setOnlineState(false);
    }
  };

  return (
    <View style={styles.wrapper}>
      <TouchableOpacity
        style={[
          styles.container,
          !isOnline && styles.offlineBg,
          isSyncing && styles.syncingBg,
        ]}
        onPress={handleToggleOnline}
        activeOpacity={0.8}
      >
        {isSyncing ? (
          <RefreshCw size={12} color="#FFF" style={styles.spinIcon} />
        ) : isOnline ? (
          <Wifi size={12} color={colors.status.success} />
        ) : (
          <WifiOff size={12} color={colors.severity.MODERATE.main} />
        )}

        <Text style={styles.text}>
          {isSyncing
            ? 'SYNCING EMERGENCY TELEMETRY...'
            : isOnline
            ? 'ONLINE • LIVE COMMAND TELEMETRY'
            : 'OFFLINE MODE • USING LOCAL CACHE'}
        </Text>

        <Text style={styles.toggleHint}>{isOnline ? '[Simulate Offline]' : '[Sync Online]'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    paddingHorizontal: spacing.md,
    marginVertical: spacing.xs,
  },
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(16, 185, 129, 0.12)',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: radius.full,
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.3)',
    gap: spacing.xs,
  },
  offlineBg: {
    backgroundColor: 'rgba(245, 158, 11, 0.12)',
    borderColor: 'rgba(245, 158, 11, 0.4)',
  },
  syncingBg: {
    backgroundColor: 'rgba(59, 130, 246, 0.15)',
    borderColor: 'rgba(59, 130, 246, 0.4)',
  },
  text: {
    color: colors.text.primary,
    fontSize: 10,
    fontWeight: typography.fontWeight.heavy,
    letterSpacing: 0.5,
    flex: 1,
  },
  toggleHint: {
    color: colors.text.muted,
    fontSize: 9,
  },
  spinIcon: {
    // Animated spin if needed
  },
});
