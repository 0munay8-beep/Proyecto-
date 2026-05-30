"""
Geospatial operations for bus routing and mapping
"""

import numpy as np
from typing import List, Tuple, Dict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from shapely.geometry import Point, LineString, Polygon
from .algebra import AlgebraOperations


class GeoOperations:
    """Geospatial operations for route planning"""

    def __init__(self):
        """Initialize geocoder"""
        self.geocoder = Nominatim(user_agent="bus_management_system")
        self.algebra = AlgebraOperations()

    def get_coordinates_from_address(self, address: str) -> Tuple[float, float]:
        """
        Get coordinates from address
        Returns (latitude, longitude)
        """
        try:
            location = self.geocoder.geocode(address)
            if location:
                return location.latitude, location.longitude
            return None, None
        except Exception as e:
            print(f"Error geocoding address: {e}")
            return None, None

    def get_address_from_coordinates(self, lat: float, lon: float) -> str:
        """
        Get address from coordinates (reverse geocoding)
        """
        try:
            location = self.geocoder.reverse(f"{lat}, {lon}")
            return location.address if location else "Unknown location"
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return "Unknown location"

    def calculate_route_distance(self, waypoints: List[Tuple[float, float]]) -> float:
        """
        Calculate total distance of route given waypoints
        Returns distance in kilometers
        """
        total_distance = 0.0
        for i in range(len(waypoints) - 1):
            lat1, lon1 = waypoints[i]
            lat2, lon2 = waypoints[i + 1]
            distance = self.algebra.haversine_distance(lat1, lon1, lat2, lon2)
            total_distance += distance
        return total_distance

    def interpolate_route_points(self, start: Tuple[float, float], end: Tuple[float, float], num_points: int = 10) -> List[Tuple[float, float]]:
        """
        Interpolate intermediate points between start and end
        """
        lat_range = np.linspace(start[0], end[0], num_points)
        lon_range = np.linspace(start[1], end[1], num_points)
        return list(zip(lat_range, lon_range))

    def point_in_polygon(self, point: Tuple[float, float], polygon_points: List[Tuple[float, float]]) -> bool:
        """
        Check if point is inside polygon (service area check)
        """
        point_geom = Point(point[1], point[0])  # Note: shapely uses (lon, lat)
        polygon_geom = Polygon([(p[1], p[0]) for p in polygon_points])
        return polygon_geom.contains(point_geom)

    def calculate_coverage_area(self, routes: List[List[Tuple[float, float]]]) -> float:
        """
        Calculate total coverage area
        """
        # Create linestrings from routes
        linestrings = [LineString([(p[1], p[0]) for p in route]) for route in routes]
        
        # Get union of all routes
        union_geom = linestrings[0] if linestrings else None
        for line in linestrings[1:]:
            union_geom = union_geom.union(line)
        
        return union_geom.length if union_geom else 0.0

    def create_heat_map_data(self, bus_locations: List[Dict], grid_size: Tuple[int, int] = (10, 10)) -> np.ndarray:
        """
        Create heat map data from bus locations
        Returns 2D numpy array for visualization
        """
        # Extract coordinates
        lats = np.array([loc['lat'] for loc in bus_locations])
        lons = np.array([loc['lon'] for loc in bus_locations])
        
        # Create histogram (heat map)
        heat_map, _, _ = np.histogram2d(lats, lons, bins=grid_size)
        
        return heat_map.T

    def get_nearest_stop(self, current_location: Tuple[float, float], stops: List[Dict]) -> Dict:
        """
        Find nearest bus stop from current location
        """
        min_distance = float('inf')
        nearest_stop = None
        
        for stop in stops:
            distance = self.algebra.haversine_distance(
                current_location[0],
                current_location[1],
                stop['lat'],
                stop['lon']
            )
            if distance < min_distance:
                min_distance = distance
                nearest_stop = {**stop, 'distance_km': distance}
        
        return nearest_stop

    def simplify_route(self, waypoints: List[Tuple[float, float]], tolerance: float = 0.001) -> List[Tuple[float, float]]:
        """
        Simplify route using Douglas-Peucker algorithm via Shapely
        """
        line = LineString([(p[1], p[0]) for p in waypoints])
        simplified = line.simplify(tolerance)
        coords = list(simplified.coords)
        return [(lat, lon) for lon, lat in coords]