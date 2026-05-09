import numpy as np
import time
from scipy.spatial.distance import cdist
import os

def nearest_neighbor_tsp_fast(points):
    """
    Simple nearest neighbor greedy construction.
    O(n²) but very fast - no optimization pass needed.
    """
    n = len(points)
    unvisited = set(range(n))
    current = 0
    tour = [current]
    unvisited.remove(current)
    
    # Build tour greedily by always picking nearest unvisited
    for _ in range(n - 1):
        # Find nearest unvisited point
        current_point = points[current]
        nearest_idx = min(unvisited, key=lambda x: np.linalg.norm(points[x] - current_point))
        tour.append(nearest_idx)
        unvisited.remove(nearest_idx)
        current = nearest_idx
    
    return tour

def nearest_neighbor_tsp_grid(points):
    """
    Grid-based nearest neighbor: divide into sections and connect greedily.
    Much faster for large point clouds.
    """
    if len(points) < 1000:
        return nearest_neighbor_tsp_fast(points)
    
    print("Using grid-based greedy construction...")
    
    # Determine grid size based on point count
    grid_size = 20  # pixels
    
    # Create grid buckets
    grid = {}
    for idx, (x, y) in enumerate(points):
        grid_key = (int(x // grid_size), int(y // grid_size))
        if grid_key not in grid:
            grid[grid_key] = []
        grid[grid_key].append(idx)
    
    # Visit grid cells in a snake pattern for locality
    tour = []
    visited_cells = set()
    
    # Start from top-left cell with points
    current_cell = min(grid.keys(), key=lambda c: (c[1], c[0]))
    
    while len(visited_cells) < len(grid):
        if current_cell in grid and current_cell not in visited_cells:
            # Add all points in this cell to tour
            cell_points = grid[current_cell]
            tour.extend(cell_points)
            visited_cells.add(current_cell)
        
        # Find nearest unvisited cell
        if len(visited_cells) < len(grid):
            unvisited_cells = [c for c in grid.keys() if c not in visited_cells]
            current_cell = min(unvisited_cells, 
                             key=lambda c: np.linalg.norm(np.array(c) - np.array(current_cell)))
    
    return tour

def tour_distance(tour, points):
    """Calculate total distance of a tour."""
    distance = 0
    for i in range(len(tour)):
        distance += np.linalg.norm(points[tour[i]] - points[tour[(i+1) % len(tour)]])
    return distance

def solve_tsp(points, time_limit=50):
    """
    Solve TSP using fast greedy nearest neighbor.
    Trades accuracy for speed - good for local connectivity.
    """
    print(f"Solving TSP for {len(points)} points...")
    start_time = time.time()
    
    # Use grid-based greedy construction (no optimization)
    print("Building tour with greedy nearest neighbor...")
    tour = nearest_neighbor_tsp_grid(points)
    
    # Calculate distance for reference
    tour_dist = tour_distance(tour, points)
    elapsed = time.time() - start_time
    
    print(f"Tour distance: {tour_dist:.2f}")
    print(f"Total time: {elapsed:.2f}s")
    
    return tour

def read_coordinates(input_path):
    """Read coordinates from file."""
    points = []
    try:
        with open(input_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(float, line.split())
                    points.append([x, y])
        return np.array(points)
    except Exception as e:
        print(f"Error reading coordinates: {e}")
        return None

def write_path(tour, points, output_path):
    """Write points in tour order to file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            for idx in tour:
                x, y = points[idx]
                x, y = int(x), int(y)  # Convert to integers for output
                f.write(f"{x} {y}\n")
        print(f"Path written to {output_path}")
    except Exception as e:
        print(f"Error writing path: {e}")

if __name__ == "__main__":
    # Configuration
    input_path = "txtfiles/points.txt"
    output_path = "txtfiles/points.txt"
    time_limit = 60  # seconds
    
    # Read points
    points = read_coordinates(input_path)
    if points is None:
        exit(1)
    
    print(f"Loaded {len(points)} points")
    
    # Solve TSP
    tour = solve_tsp(points, time_limit=time_limit)
    
    # Write result
    write_path(tour, points, output_path)