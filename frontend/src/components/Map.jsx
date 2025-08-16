import { useState, useEffect } from 'react';
import { Viewer, Entity, CameraFlyTo } from 'resium';
import { Cartesian3 } from 'cesium';
import axios from 'axios';
import opencage from 'opencage-api-client';

// This is required by Resium to point to the Cesium assets
// The vite-plugin-cesium should handle serving them
window.CESIUM_BASE_URL = '/cesium/';

const Map = ({ locationString }) => {
  const [coordinates, setCoordinates] = useState(null);
  const [error, setError] = useState(null);
  const [apiKeys, setApiKeys] = useState(null);

  // 1. Fetch API keys from our backend
  useEffect(() => {
    const fetchKeys = async () => {
      try {
        const { data } = await axios.get('http://localhost:3000/api/config');
        setApiKeys(data);
      } catch (err) {
        setError('Failed to load map configuration.');
      }
    };
    fetchKeys();
  }, []);

  // 2. Geocode the location string once we have keys
  useEffect(() => {
    if (apiKeys && locationString) {
      const geocode = async () => {
        try {
          const data = await opencage.geocode({
            q: locationString,
            key: apiKeys.openCageToken,
            limit: 1,
          });

          if (data.results && data.results.length > 0) {
            const { lat, lng } = data.results[0].geometry;
            // Cesium uses Cartesian3, not lat/lng directly
            setCoordinates(Cartesian3.fromDegrees(lng, lat, 15000)); // longitude, latitude, height
          } else {
            setError(`Could not find coordinates for "${locationString}"`);
          }
        } catch (err) {
          setError('Geocoding failed. Please check the location string.');
          console.error(err);
        }
      };
      geocode();
    }
  }, [apiKeys, locationString]);

  if (error) {
    return <div className="map-error">Error: {error}</div>;
  }
  
  if (!apiKeys) {
    // Don't show the geocoding message until we have keys
    return <div className="map-loading">Loading Map...</div>;
  }

  return (
    <Viewer style={{ width: '100%', height: '100%' }}>
      {coordinates && (
        <>
          <Entity
            position={coordinates}
            name={locationString}
            point={{ pixelSize: 10 }}
            description="Listing Location"
          />
          <CameraFlyTo destination={coordinates} duration={3} />
        </>
      )}
    </Viewer>
  );
};

export default Map;
