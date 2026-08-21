import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Header } from '../../src/components/common/Header';
import { ConnectionStatus } from '../../src/components/common/ConnectionStatus';
import { ShelterCard } from '../../src/components/civilian/ShelterCard';
import { useDisasterStore } from '../../src/store/useDisasterStore';
import { colors, typography, spacing, radius } from '../../src/theme';
import { useRouter } from 'expo-router';
import { Search, Filter, Home } from 'lucide-react-native';
import { Shelter } from '../../src/types';

export default function SheltersScreen() {
  const router = useRouter();
  const { shelters, calculateSafeRoute } = useDisasterStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<'ALL' | 'OPEN' | 'MEDICAL' | 'FOOD'>('ALL');

  const filteredShelters = shelters.filter((shelter) => {
    const matchesSearch =
      shelter.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      shelter.address.toLowerCase().includes(searchQuery.toLowerCase());

    if (selectedFilter === 'OPEN') return matchesSearch && shelter.status === 'OPEN';
    if (selectedFilter === 'MEDICAL') return matchesSearch && shelter.amenities.medicalKit;
    if (selectedFilter === 'FOOD') return matchesSearch && shelter.amenities.foodSupplies;
    return matchesSearch;
  });

  const handleRouteToShelter = async (shelter: Shelter) => {
    await calculateSafeRoute({ latitude: 22.3072, longitude: 73.1812 }, shelter.id);
    router.push('/civilian/evacuation' as any);
  };

  return (
    <SafeAreaView style={styles.container}>
      <Header title="SHELTER DIRECTORY" />
      <ConnectionStatus />

      <View style={styles.content}>
        {/* Search Input Bar */}
        <View style={styles.searchBar}>
          <Search size={16} color={colors.text.muted} />
          <TextInput
            style={styles.searchInput}
            placeholder="Search nearby shelters by name or address..."
            placeholderTextColor={colors.text.muted}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {/* Filter Chips Row */}
        <View style={styles.filterRow}>
          {[
            { key: 'ALL', label: 'All Camps' },
            { key: 'OPEN', label: 'Available Only' },
            { key: 'MEDICAL', label: 'Medical Desk' },
            { key: 'FOOD', label: 'Food Rations' },
          ].map((item) => (
            <TouchableOpacity
              key={item.key}
              style={[
                styles.filterChip,
                selectedFilter === item.key && styles.filterChipActive,
              ]}
              onPress={() => setSelectedFilter(item.key as any)}
            >
              <Text
                style={[
                  styles.filterText,
                  selectedFilter === item.key && styles.filterTextActive,
                ]}
              >
                {item.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <FlatList
          data={filteredShelters}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <ShelterCard shelter={item} onNavigate={handleRouteToShelter} />
          )}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
        />
      </View>
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
    paddingHorizontal: spacing.md,
    paddingTop: spacing.md,
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.background.secondary,
    borderRadius: radius.md,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderWidth: 1,
    borderColor: colors.border.subtle,
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
  searchInput: {
    flex: 1,
    color: colors.text.primary,
    fontSize: typography.fontSize.sm,
  },
  filterRow: {
    flexDirection: 'row',
    gap: spacing.xs,
    marginBottom: spacing.md,
  },
  filterChip: {
    backgroundColor: colors.background.secondary,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: radius.full,
    borderWidth: 1,
    borderColor: colors.border.subtle,
  },
  filterChipActive: {
    backgroundColor: colors.primary.main,
    borderColor: colors.primary.light,
  },
  filterText: {
    color: colors.text.secondary,
    fontSize: 11,
    fontWeight: typography.fontWeight.semibold,
  },
  filterTextActive: {
    color: '#FFF',
    fontWeight: typography.fontWeight.bold,
  },
  listContent: {
    paddingBottom: spacing.xxl,
  },
});
