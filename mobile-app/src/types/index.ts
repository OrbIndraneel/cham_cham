export interface HazardZone {
  districtId: string;
  primaryHazard: string;
  secondaryCascadeHazard: string;
  cascadeProbability: number;
  estimatedLeadTimeMins: number;
  riskLevel: 'High' | 'Medium' | 'Low';
  polygonCoordinates: Array<[number, number]>;
}

export interface Shelter {
  shelterId: string;
  name: string;
  latitude: number;
  longitude: number;
  capacity: number;
  currentOccupancy: number;
  status: 'Open' | 'Full' | 'Closed';
}

export interface EvacuationRoute {
  routeId: string;
  distanceKm: number;
  estimatedTimeMins: number;
  hazardAvoided: boolean;
  routeCoordinates: Array<[number, number]>;
}
