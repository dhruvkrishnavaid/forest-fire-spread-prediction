import numpy as np
from typing import Dict, List, Tuple
import rasterio
from rasterio.transform import from_bounds

class CellularAutomataSimulator:
    def __init__(self, grid_size: Tuple[int, int] = (1000, 1000)):
        self.grid_size = grid_size
        self.cell_size = 30  # 30m resolution
        
    async def simulate_fire_spread(
        self,
        initial_fire_points: List[Tuple[int, int]],
        wind_data: Dict,
        terrain_data: np.ndarray,
        fuel_data: np.ndarray,
        time_steps: List[int]
    ) -> Dict[int, np.ndarray]:
        """
        Simulate fire spread using cellular automata
        """
        # Initialize grid
        fire_grid = np.zeros(self.grid_size, dtype=np.float32)
        
        # Set initial fire points
        for point in initial_fire_points:
            fire_grid[point[0], point[1]] = 1.0
        
        results = {}
        current_grid = fire_grid.copy()
        
        for hour in time_steps:
            # Simulate spread for each hour
            for _ in range(hour * 60):  # 60 minutes per hour
                current_grid = self._spread_step(
                    current_grid, wind_data, terrain_data, fuel_data
                )
            
            results[hour] = current_grid.copy()
        
        return results
    
    def _spread_step(
        self,
        fire_grid: np.ndarray,
        wind_data: Dict,
        terrain_data: np.ndarray,
        fuel_data: np.ndarray
    ) -> np.ndarray:
        """
        Single time step of fire spread simulation
        """
        new_grid = fire_grid.copy()
        
        # Apply cellular automata rules
        for i in range(1, fire_grid.shape[0] - 1):
            for j in range(1, fire_grid.shape[1] - 1):
                if fire_grid[i, j] == 0:  # Non-burning cell
                    # Check neighbors
                    neighbors = fire_grid[i-1:i+2, j-1:j+2]
                    
                    # Calculate spread probability
                    spread_prob = self._calculate_spread_probability(
                        neighbors, wind_data, terrain_data[i, j], fuel_data[i, j]
                    )
                    
                    if np.random.random() < spread_prob:
                        new_grid[i, j] = 1.0
        
        return new_grid
    
    def _calculate_spread_probability(
        self,
        neighbors: np.ndarray,
        wind_data: Dict,
        terrain_slope: float,
        fuel_load: float
    ) -> float:
        """
        Calculate probability of fire spread to a cell
        """
        # Base probability from burning neighbors
        burning_neighbors = np.sum(neighbors > 0)
        base_prob = min(burning_neighbors * 0.1, 0.8)
        
        # Wind effect
        wind_factor = 1 + (wind_data['speed'] / 50.0)  # Normalize wind speed
        
        # Terrain effect (uphill spreads faster)
        terrain_factor = 1 + (terrain_slope / 45.0)  # Normalize slope
        
        # Fuel effect
        fuel_factor = fuel_load / 100.0  # Normalize fuel load
        
        # Combined probability
        total_prob = base_prob * wind_factor * terrain_factor * fuel_factor
        
        return min(total_prob, 1.0)
