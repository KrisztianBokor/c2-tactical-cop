import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { useQuery } from '@tanstack/react-query';

interface TrackDTO {
  id: string;
  classification: 'FRIENDLY' | 'HOSTILE' | 'UNKNOWN';
  lat: number;
  lon: number;
  speed: number;
  altitude: number;
  heading: number;
  timestamp: string;
}

const fetchCOP = async (): Promise<TrackDTO[]> => {
  const res = await fetch('http://localhost:8080/api/v1/c2/cop/latest');
  if (!res.ok) {
    throw new Error('Failed to fetch tactical feed');
  }
  return res.json();
};

const getMarkerIcon = (classification: TrackDTO['classification']) => {
  let bgColor = '#3b82f6'; // FRIENDLY: Blue
  if (classification === 'HOSTILE') bgColor = '#ef4444'; // HOSTILE: Red
  if (classification === 'UNKNOWN') bgColor = '#f59e0b'; // UNKNOWN: Amber

  return L.divIcon({
    className: 'custom-tactical-marker',
    html: `<div style="background-color: ${bgColor}; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ffffff; font-size: 10px;">•</div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
};

export const TacticalMap: React.FC = () => {
  const { data: tracks = [], isError, error } = useQuery({
    queryKey: ['tactical-cop'],
    queryFn: fetchCOP,
    refetchInterval: 2000, // Poll every 2 seconds
  });

  return (
    <div style={{ position: 'relative', width: '100%', height: 'calc(100vh - 60px)' }}>
      {isError && (
        <div style={{ position: 'absolute', top: 10, right: 10, zIndex: 1000, background: '#ef4444', padding: '8px 16px', borderRadius: 4 }}>
          Feed error: {(error as Error).message}
        </div>
      )}

      <MapContainer
        center={[53.0, 5.5]}
        zoom={7}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>'
  url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
/>
        {tracks.map((track) => (
          <Marker
            key={track.id}
            position={[track.lat, track.lon]}
            icon={getMarkerIcon(track.classification)}
          >
            <Popup>
              <div style={{ color: '#0f172a', minWidth: '150px' }}>
                <h3 style={{ margin: '0 0 4px', fontSize: '14px' }}>{track.id}</h3>
                <p><strong>Status:</strong> {track.classification}</p>
                <p><strong>Speed:</strong> {track.speed} kts</p>
                <p><strong>Altitude:</strong> {track.altitude} m</p>
                <p><strong>Heading:</strong> {track.heading}°</p>
                <p style={{ fontSize: '10px', color: '#64748b' }}>{track.timestamp}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};