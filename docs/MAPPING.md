# 🗺️ MAPPING.md - Guía de Mapas Interactivos

## Tabla de Contenidos
1. [Tecnologías](#tecnologías)
2. [Configuración Inicial](#configuración-inicial)
3. [Componentes React](#componentes-react)
4. [Integraciones](#integraciones)
5. [Casos de Uso](#casos-de-uso)
6. [Troubleshooting](#troubleshooting)

---

## Tecnologías

### Stack Principal
- **Leaflet.js** - Mapas interactivos de código abierto
- **React-Leaflet** - Componentes React para Leaflet
- **Mapbox GL** - Capas de vector tiles (opcional)
- **Geolocation API** - Posicionamiento GPS del usuario
- **Cluster.js** - Agrupación de marcadores

### Proveedores de Tiles
```javascript
// OpenStreetMap (Gratuito)
https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png

// CartoDB (Calidad superior)
https://{s}.basemaps.cartocdn.com/positron/{z}/{x}/{y}{r}.png

// Mapbox (Premium)
https://api.mapbox.com/styles/v1/{username}/{style_id}/static/...
```

---

## Configuración Inicial

### 1. Instalación de Dependencias

```bash
npm install leaflet react-leaflet leaflet-cluster geolocation-utils
npm install --save-dev @types/leaflet
```

### 2. Importar CSS en `App.jsx`

```javascript
import 'leaflet/dist/leaflet.css';
import 'leaflet-cluster/dist/MarkerCluster.css';
```

### 3. Variable de Entorno

```env
REACT_APP_MAPBOX_TOKEN=pk_test_tu_token_aqui
REACT_APP_OPEN_ROUTE_SERVICE_KEY=tu_key_aqui
```

---

## Componentes React

### MapContainer Principal

```jsx
import { MapContainer, TileLayer, Popup, Marker, useMap } from 'react-leaflet';
import { LatLngBounds } from 'leaflet';

export function TransportMap({ buses, routes, stops }) {
  const [userLocation, setUserLocation] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      position => {
        setUserLocation([
          position.coords.latitude,
          position.coords.longitude
        ]);
      }
    );
  }, []);

  return (
    <MapContainer
      center={[40.4168, -3.7038]} // Madrid
      zoom={13}
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <BusMarkers buses={buses} />
      <RoutePolylines routes={routes} />
      <StopMarkers stops={stops} />
      {userLocation && <UserMarker position={userLocation} />}
    </MapContainer>
  );
}
```

### Componente: Marcadores de Buses

```jsx
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

export function BusMarkers({ buses }) {
  const busIcon = L.icon({
    iconUrl: '/icons/bus-blue.svg',
    iconSize: [32, 32],
    popupAnchor: [0, -16]
  });

  return buses.map(bus => (
    <Marker
      key={bus.id}
      position={[bus.latitude, bus.longitude]}
      icon={busIcon}
      title={`Bus ${bus.number}`}
    >
      <Popup>
        <div className="bus-popup">
          <h3>Línea {bus.number}</h3>
          <p>📍 {bus.current_stop}</p>
          <p>🚍 {bus.passengers} pasajeros</p>
          <p>⏱️ Próxima parada en 3 min</p>
        </div>
      </Popup>
    </Marker>
  ));
}
```

### Componente: Rutas Polilineales

```jsx
import { Polyline, Popup } from 'react-leaflet';
import { useState } from 'react';

export function RoutePolylines({ routes }) {
  const [hoveredRoute, setHoveredRoute] = useState(null);

  const getRouteColor = (routeNumber) => {
    const colors = {
      '1': '#FF0000',
      '2': '#00FF00',
      '3': '#0000FF',
      '4': '#FFFF00',
      'default': '#808080'
    };
    return colors[routeNumber] || colors.default;
  };

  return routes.map(route => (
    <Polyline
      key={route.id}
      positions={route.coordinates.map(c => [c.lat, c.lng])}
      color={getRouteColor(route.number)}
      weight={hoveredRoute === route.id ? 4 : 2}
      opacity={hoveredRoute === route.id ? 0.9 : 0.6}
      onMouseOver={() => setHoveredRoute(route.id)}
      onMouseOut={() => setHoveredRoute(null)}
    >
      <Popup>
        <div className="route-popup">
          <h3>Ruta {route.number}</h3>
          <p>📍 {route.origin} → {route.destination}</p>
          <p>🕐 {route.duration} minutos</p>
          <p>👥 {route.daily_passengers} pasajeros/día</p>
        </div>
      </Popup>
    </Polyline>
  ));
}
```

### Componente: Mapa de Calor (Congestión)

```jsx
import { useEffect } from 'react';
import L from 'leaflet';

export function HeatmapLayer({ congestionData }) {
  const map = useMap();

  useEffect(() => {
    const heatLayer = L.heatLayer(
      congestionData.map(point => [
        point.lat,
        point.lng,
        point.intensity // 0-1
      ]),
      {
        radius: 25,
        blur: 15,
        maxZoom: 1,
        minOpacity: 0.2,
        gradient: {
          0.2: '#0000FF',
          0.5: '#00FF00',
          0.7: '#FFFF00',
          1: '#FF0000'
        }
      }
    ).addTo(map);

    return () => map.removeLayer(heatLayer);
  }, [congestionData, map]);

  return null;
}
```

### Componente: Búsqueda de Paradas Cercanas

```jsx
import { useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';

export function NearbyStopsSearch({ radius = 500 }) {
  const map = useMap();
  const [nearbyStops, setNearbyStops] = useState([]);

  useEffect(() => {
    if (!map) return;

    const userLat = map.getCenter().lat;
    const userLng = map.getCenter().lng;

    // Llamar a geo.py backend
    fetch(`/api/geo/nearby-stops?lat=${userLat}&lng=${userLng}&radius=${radius}`)
      .then(r => r.json())
      .then(data => setNearbyStops(data))
      .catch(err => console.error('Error:', err));
  }, [map, radius]);

  return nearbyStops.map(stop => (
    <Marker key={stop.id} position={[stop.lat, stop.lng]} />
  ));
}
```

---

## Integraciones

### 1. Integración con Backend (API)

```javascript
// src/api/mapAPI.js
export const mapAPI = {
  getBuses: async () => {
    const res = await fetch('/api/buses/realtime');
    return res.json();
  },

  getRoutes: async () => {
    const res = await fetch('/api/routes');
    return res.json();
  },

  getStops: async () => {
    const res = await fetch('/api/stops');
    return res.json();
  },

  getCongestion: async (routeId) => {
    const res = await fetch(`/api/analytics/congestion/${routeId}`);
    return res.json();
  },

  getNearbyStops: async (lat, lng, radius = 500) => {
    const res = await fetch(
      `/api/geo/nearby-stops?lat=${lat}&lng=${lng}&radius=${radius}`
    );
    return res.json();
  },

  calculateRoute: async (startLat, startLng, endLat, endLng) => {
    const res = await fetch('/api/geo/route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        start: { lat: startLat, lng: startLng },
        end: { lat: endLat, lng: endLng }
      })
    });
    return res.json();
  }
};
```

### 2. WebSocket para Actualizaciones en Tiempo Real

```javascript
// src/hooks/useRealTimeMap.js
import { useEffect, useState } from 'react';

export function useRealTimeMap() {
  const [buses, setBuses] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/buses');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setBuses(data.buses);
    };

    return () => ws.close();
  }, []);

  return { buses };
}
```

### 3. Geocodificación

```javascript
// src/utils/geocoding.js
export async function geocodeAddress(address) {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json`
  );
  const data = await res.json();
  return data[0] ? { lat: data[0].lat, lng: data[0].lon } : null;
}

export async function reverseGeocode(lat, lng) {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`
  );
  return res.json();
}
```

---

## Casos de Uso

### 1. Dashboard de Gerencia
```jsx
<TransportMap
  buses={realtimeBuses}
  routes={allRoutes}
  stops={allStops}
  heatmapMode={true}
  congestionOverlay={true}
/>
```

### 2. Aplicación de Pasajeros
```jsx
<PassengerMap
  userLocation={myLocation}
  nearestStops={nearbyStops}
  selectedRoute={routeId}
  estimatedArrival={eta}
/>
```

### 3. Planificación de Rutas
```jsx
<RouteDesignMap
  editMode={true}
  snapToRoads={true}
  obstacleDetection={true}
/>
```

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Mapas no cargan | Verificar token de Mapbox, CORS headers |
| Marcadores superpuestos | Usar clustering (markercluster.js) |
| Rendimiento lento | Implementar virtualización, lazy loading |
| Geolocalización no funciona | HTTPS requerido, permisos del navegador |
| Rutas no se actualizan | Verificar WebSocket connection, polling fallback |

---

## Referencias
- [Leaflet Documentation](https://leafletjs.com/)
- [React-Leaflet Guide](https://react-leaflet.js.org/)
- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
