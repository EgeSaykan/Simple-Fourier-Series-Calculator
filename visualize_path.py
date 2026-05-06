import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import os

def read_coordinates(input_path):
    """Read coordinates from file."""
    points = []
    try:
        with open(input_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(float, line.split())
                    points.append([int(x), int(y)])
        return np.array(points)
    except Exception as e:
        print(f"Error reading coordinates: {e}")
        return None

def read_path_order(path_file):
    """Read the order of point indices from the path file."""
    try:
        with open(path_file, 'r') as f:
            indices = [int(line.strip()) for line in f if line.strip()]
        return indices
    except Exception as e:
        print(f"Error reading path: {e}")
        return None

def create_animated_path(image_path, coordinates, path_order, output_gif, frame_skip=1):
    """
    Create an animated GIF showing the path being drawn progressively.
    """
    # Load original image
    try:
        orig_img = Image.open(image_path)
        width, height = orig_img.size
        bg_image = np.array(orig_img.convert('RGB'))
    except Exception as e:
        print(f"Error loading original image: {e}")
        return
    
    # Create frames for animation
    frames = []
    
    # Start with the original image
    current_canvas = bg_image.copy()
    frames.append(Image.fromarray(current_canvas))
    
    print(f"Creating animation frames ({len(path_order)} points)...")
    
    # Draw the path progressively
    for step in range(0, len(path_order), max(1, frame_skip)):
        current_canvas = bg_image.copy()
        
        # Draw all path segments up to this point
        for i in range(step):
            idx1 = path_order[i]
            idx2 = path_order[(i + 1) % len(path_order)]
            
            x1, y1 = coordinates[idx1]
            x2, y2 = coordinates[idx2]
            
            # Draw line between points
            draw_line(current_canvas, x1, y1, x2, y2, color=(0, 150, 255))
        
        # Highlight current position
        if step < len(path_order):
            idx = path_order[step]
            x, y = coordinates[idx]
            draw_circle(current_canvas, x, y, radius=3, color=(255, 0, 0))
        
        frames.append(Image.fromarray(current_canvas))
        
        if (step + 1) % max(100, len(path_order) // 10) == 0:
            print(f"  Frame {step + 1}/{len(path_order)}")
    
    # Save as GIF
    print(f"Saving animation to {output_gif}...")
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=10,  # milliseconds per frame
        loop=0  # loop forever
    )
    print(f"Animation saved: {output_gif}")

def draw_line(canvas, x1, y1, x2, y2, color, thickness=2):
    """Draw a line on canvas using Bresenham's algorithm."""
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    err = dx - dy
    
    h, w = canvas.shape[:2]
    
    while True:
        if 0 <= x1 < w and 0 <= y1 < h:
            # Draw thick line
            for tx in range(-thickness//2, thickness//2 + 1):
                for ty in range(-thickness//2, thickness//2 + 1):
                    nx, ny = x1 + tx, y1 + ty
                    if 0 <= nx < w and 0 <= ny < h:
                        canvas[ny, nx] = color
        
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_circle(canvas, x, y, radius=3, color=(255, 0, 0)):
    """Draw a filled circle on canvas."""
    x, y, radius = int(x), int(y), int(radius)
    h, w = canvas.shape[:2]
    
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx*dx + dy*dy <= radius*radius:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    canvas[ny, nx] = color

def create_fast_animation(image_path, coordinates, path_order, output_gif):
    """
    Create animation by sampling frames strategically.
    """
    # Load original image
    try:
        orig_img = Image.open(image_path)
        width, height = orig_img.size
        bg_image = np.array(orig_img.convert('RGB'))
    except Exception as e:
        print(f"Error loading original image: {e}")
        return
    
    frames = []
    n_points = len(path_order)
    
    # Create 100-200 frames for smooth animation
    n_frames = min(200, max(50, n_points // 50))
    frame_indices = np.linspace(0, n_points, n_frames, dtype=int)
    
    print(f"Creating animation with {n_frames} frames...")
    
    for frame_num, step in enumerate(frame_indices):
        current_canvas = bg_image.copy()
        
        # Draw all path segments up to this point
        for i in range(min(step, n_points - 1)):
            idx1 = path_order[i]
            idx2 = path_order[i + 1]
            
            x1, y1 = coordinates[idx1]
            x2, y2 = coordinates[idx2]
            
            # Draw line between points
            draw_line(current_canvas, x1, y1, x2, y2, color=(0, 150, 255), thickness=2)
        
        # Highlight current position
        if step < n_points:
            idx = path_order[step]
            x, y = coordinates[idx]
            draw_circle(current_canvas, x, y, radius=3, color=(255, 0, 0))
        
        frames.append(Image.fromarray(current_canvas))
        
        if (frame_num + 1) % max(1, n_frames // 5) == 0:
            print(f"  Frame {frame_num + 1}/{n_frames}")
    
    # Save as GIF
    print(f"Saving animation to {output_gif}...")
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=50,  # milliseconds per frame
        loop=0  # loop forever
    )
    print(f"Animation saved: {output_gif}")

if __name__ == "__main__":
    # Configuration
    image_path = "image_cleaned.jpg"
    coordinates_file = "txtfiles/points.txt"
    path_file = "txtfiles/shortest_path.txt"
    output_gif = "txtfiles/path_animation.gif"
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        exit(1)
    
    if not os.path.exists(coordinates_file):
        print(f"Error: {coordinates_file} not found (run image_to_coordinates.py first)")
        exit(1)
    
    if not os.path.exists(path_file):
        print(f"Error: {path_file} not found (run shortest_path_maker.py first)")
        exit(1)
    
    print("Loading data...")
    coordinates = read_coordinates(coordinates_file)
    path_order = read_path_order(path_file)
    
    if coordinates is None or path_order is None:
        exit(1)
    
    print(f"Loaded {len(coordinates)} points and {len(path_order)} path segments")
    
    # Create animation
    print("Creating animated visualization...")
    create_fast_animation(image_path, coordinates, path_order, output_gif)
