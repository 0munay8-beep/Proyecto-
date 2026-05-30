"""
Linear Algebra Operations for advanced calculations
"""

import numpy as np
from typing import List, Tuple
from scipy.spatial.distance import cdist
from scipy.linalg import svd


class AlgebraOperations:
    """Linear algebra operations using NumPy and SciPy"""

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS points using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth radius in km
        
        lat1_rad = np.radians(lat1)
        lon1_rad = np.radians(lon1)
        lat2_rad = np.radians(lat2)
        lon2_rad = np.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c

    @staticmethod
    def matrix_rotation(points: List[Tuple[float, float]], angle: float) -> np.ndarray:
        """
        Rotate points using rotation matrix
        angle: rotation angle in radians
        Returns rotated points as numpy array
        """
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        
        rotation_matrix = np.array([
            [cos_a, -sin_a],
            [sin_a, cos_a]
        ])
        
        points_array = np.array(points)
        return points_array @ rotation_matrix.T

    @staticmethod
    def eigenvalue_congestion_analysis(congestion_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Use eigenvalues to analyze congestion patterns
        Returns eigenvalues and eigenvectors
        """
        # Create covariance matrix
        cov_matrix = np.cov(congestion_data.T)
        
        # Get eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Sort by eigenvalues
        idx = eigenvalues.argsort()[::-1]
        
        return eigenvalues[idx], eigenvectors[:, idx]

    @staticmethod
    def svd_dimensionality_reduction(data: np.ndarray, n_components: int) -> np.ndarray:
        """
        Reduce dimensionality using Singular Value Decomposition
        """
        U, S, Vt = svd(data, full_matrices=False)
        
        # Keep top n components
        return U[:, :n_components] @ np.diag(S[:n_components])

    @staticmethod
    def polyfit_route_interpolation(waypoints: List[Tuple[float, float]], degree: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit polynomial to route waypoints for smooth interpolation
        """
        waypoints_array = np.array(waypoints)
        x = waypoints_array[:, 0]
        y = waypoints_array[:, 1]
        
        # Fit polynomials
        lat_coef = np.polyfit(x, y[:, 0], degree) if len(y.shape) > 1 else np.polyfit(x, y, degree)
        lon_coef = np.polyfit(x, y[:, 1], degree) if len(y.shape) > 1 else lat_coef
        
        return lat_coef, lon_coef

    @staticmethod
    def linear_regression_prediction(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Linear regression for time prediction
        Returns coefficients and R-squared value
        """
        # Add bias term
        X_with_bias = np.column_stack([np.ones(len(X)), X])
        
        # Normal equation: (X^T X)^-1 X^T y
        coefficients = np.linalg.lstsq(X_with_bias, y, rcond=None)[0]
        
        # Calculate R-squared
        y_pred = X_with_bias @ coefficients
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return coefficients, r_squared

    @staticmethod
    def distance_matrix(points: List[Tuple[float, float]]) -> np.ndarray:
        """
        Calculate pairwise distance matrix between all points
        """
        points_array = np.array(points)
        return cdist(points_array, points_array, metric='euclidean')

    @staticmethod
    def zscore_anomaly_detection(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """
        Detect anomalies using Z-score method
        Returns boolean array of anomalies
        """
        mean = np.mean(data)
        std = np.std(data)
        z_scores = np.abs((data - mean) / std)
        return z_scores > threshold