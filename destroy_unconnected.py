import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import ndimage

# Configuration
TILE_SIZE = 50
IMAGE_PATH = "faces_with_detail.jpg"
OUTPUT_PATH = "image_cleaned.jpg"
MIN_EDGES_TO_KEEP = 2  # Keep components that touch 2+ edges of the tile


def load_image(path):
    """Load image and convert to binary (grayscale threshold)."""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    
    # Ensure binary: white edges on black background
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    print(f"Image loaded: {binary.shape}, dtype: {binary.dtype}")
    return binary


def visualize_tiles(image, tile_size=TILE_SIZE, title="Image Tiles"):
    """Display image broken into tiles with grid overlay."""
    h, w = image.shape
    tiles_y = (h + tile_size - 1) // tile_size
    tiles_x = (w + tile_size - 1) // tile_size
    
    # Create figure to show first few tiles (or all if small)
    max_display = min(4, tiles_y) * min(4, tiles_x)  # Show up to 4x4 grid
    
    fig, axes = plt.subplots(min(4, tiles_y), min(4, tiles_x), figsize=(12, 12))
    if min(4, tiles_y) == 1 and min(4, tiles_x) == 1:
        axes = np.array([[axes]])
    elif min(4, tiles_y) == 1 or min(4, tiles_x) == 1:
        axes = axes.reshape((min(4, tiles_y), min(4, tiles_x)))
    
    idx = 0
    for ty in range(min(4, tiles_y)):
        for tx in range(min(4, tiles_x)):
            y_start = ty * tile_size
            x_start = tx * tile_size
            y_end = min(y_start + tile_size, h)
            x_end = min(x_start + tile_size, w)
            
            tile = image[y_start:y_end, x_start:x_end]
            axes[ty, tx].imshow(tile, cmap='gray')
            axes[ty, tx].set_title(f"Tile ({ty}, {tx})")
            axes[ty, tx].axis('off')
            idx += 1
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


def touches_edges(component_mask, tile_shape):
    """
    Determine which edges of the tile the component touches.
    Returns set of edge names: {'top', 'bottom', 'left', 'right'}
    """
    edges_touched = set()
    h, w = tile_shape
    
    # Check top edge
    if np.any(component_mask[0, :]):
        edges_touched.add('top')
    
    # Check bottom edge
    if np.any(component_mask[-1, :]):
        edges_touched.add('bottom')
    
    # Check left edge
    if np.any(component_mask[:, 0]):
        edges_touched.add('left')
    
    # Check right edge
    if np.any(component_mask[:, -1]):
        edges_touched.add('right')
    
    return edges_touched


def filter_tile(tile):
    """
    Filter a single 50x50 tile:
    - Find connected components (8-connectivity)
    - Remove islands that touch < 2 edges
    - Return cleaned tile
    """
    # Find connected components with 8-connectivity
    num_features, labeled = cv2.connectedComponents(tile, connectivity=8)
    
    # Create output mask (start with all white, remove islands)
    cleaned = tile.copy()
    
    # Label 0 is background (black), labels 1+ are components
    for label in range(1, num_features):
        component_mask = (labeled == label)
        edges = touches_edges(component_mask, tile.shape)
        
        # If component doesn't touch at least 2 edges, remove it (mark as black)
        if len(edges) < MIN_EDGES_TO_KEEP:
            cleaned[component_mask] = 0  # Remove this island
    
    return cleaned


def process_image(image, tile_size=TILE_SIZE):
    """
    Process entire image tile by tile, removing disconnected islands.
    Returns cleaned image and list of modified tiles.
    """
    h, w = image.shape
    cleaned_image = np.zeros_like(image)
    modified_tiles = []  # Track which tiles were modified
    
    print(f"Processing image: {h}x{w} into {tile_size}x{tile_size} tiles")
    
    # Process each tile
    for ty in range(0, h, tile_size):
        for tx in range(0, w, tile_size):
            # Extract tile (handle edge cases where tile extends beyond image)
            y_end = min(ty + tile_size, h)
            x_end = min(tx + tile_size, w)
            tile = image[ty:y_end, tx:x_end]
            
            # Filter the tile
            cleaned_tile = filter_tile(tile)
            
            # Check if tile was modified
            if not np.array_equal(tile, cleaned_tile):
                modified_tiles.append({
                    'pos': (ty // tile_size, tx // tile_size),
                    'original': tile.copy(),
                    'cleaned': cleaned_tile.copy()
                })
            
            # Place back in cleaned image
            cleaned_image[ty:y_end, tx:x_end] = cleaned_tile
            
            print(f"  Processed tile ({ty//tile_size}, {tx//tile_size})")
    
    print(f"\n  Total tiles modified: {len(modified_tiles)}")
    return cleaned_image, modified_tiles


def display_comparison(original, cleaned, tile_size=TILE_SIZE):
    """Display original and cleaned images side-by-side with grid overlay."""
    h, w = original.shape
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Original with grid
    ax1.imshow(original, cmap='gray')
    ax1.set_title("Original Image")
    for y in range(0, h, tile_size):
        ax1.axhline(y, color='red', linewidth=0.5, alpha=0.3)
    for x in range(0, w, tile_size):
        ax1.axvline(x, color='red', linewidth=0.5, alpha=0.3)
    ax1.axis('off')
    
    # Cleaned with grid
    ax2.imshow(cleaned, cmap='gray')
    ax2.set_title("Cleaned Image (Islands Removed)")
    for y in range(0, h, tile_size):
        ax2.axhline(y, color='green', linewidth=0.5, alpha=0.3)
    for x in range(0, w, tile_size):
        ax2.axvline(x, color='green', linewidth=0.5, alpha=0.3)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()


def display_modified_tiles(modified_tiles):
    """Display before/after comparison for only the tiles that were modified."""
    if not modified_tiles:
        print("  No tiles were modified!")
        return
    
    # Show first 16 modified tiles (8x2 grid per page)
    num_to_show = min(16, len(modified_tiles))
    rows = (num_to_show + 7) // 8  # 8 tiles per row
    cols = min(8, num_to_show)
    
    fig, axes = plt.subplots(rows, cols * 2, figsize=(16, 4 * rows))
    if rows == 1 and cols == 1:
        axes = axes.reshape((1, 2))
    elif rows == 1:
        axes = axes.reshape((1, -1))
    
    for idx, tile_info in enumerate(modified_tiles[:num_to_show]):
        ax_orig = axes[idx // 8, (idx % 8) * 2]
        ax_clean = axes[idx // 8, (idx % 8) * 2 + 1]
        
        ty, tx = tile_info['pos']
        ax_orig.imshow(tile_info['original'], cmap='gray')
        ax_orig.set_title(f"Tile ({ty},{tx}) - Original")
        ax_orig.axis('off')
        
        ax_clean.imshow(tile_info['cleaned'], cmap='gray')
        ax_clean.set_title(f"Tile ({ty},{tx}) - Cleaned")
        ax_clean.axis('off')
    
    plt.suptitle(f"Modified Tiles (showing {num_to_show} of {len(modified_tiles)})")
    plt.tight_layout()
    plt.show()


class InteractiveImageEditor:
    """Interactive tool to add/remove areas from the cleaned image."""
    
    def __init__(self, original, cleaned, original_full):
        self.original = original
        self.cleaned = cleaned.copy()
        self.current_display = cleaned.copy()
        self.original_full = original_full
        self.drawing = False
        self.start_point = None
        self.rectangles = []
        self.mode = 'remove'  # 'remove' or 'restore'
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.suptitle("Interactive Editor: Click & drag to select areas. 'R' to remove, 'S' to restore, 'ENTER' to save, 'ESC' to cancel")
        
        # Draw initial images
        self.im1 = self.ax1.imshow(original, cmap='gray')
        self.ax1.set_title("Original Image")
        self.ax1.axis('off')
        
        self.im2 = self.ax2.imshow(self.current_display, cmap='gray')
        self.ax2.set_title("Cleaned Image (Edit Mode)")
        self.ax2.axis('off')
        
        # Connect events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        self.rect_artist = None
        self.result = None
        self.saved = False
        
    def on_press(self, event):
        if event.inaxes != self.ax2:
            return
        self.drawing = True
        self.start_point = (int(event.xdata), int(event.ydata))
        
    def on_release(self, event):
        if not self.drawing or self.start_point is None:
            return
        self.drawing = False
        
        end_point = (int(event.xdata), int(event.ydata))
        x1, y1 = self.start_point
        x2, y2 = end_point
        
        # Normalize coordinates
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        
        # Ensure valid region
        x_min = max(0, x_min)
        x_max = min(self.current_display.shape[1], x_max)
        y_min = max(0, y_min)
        y_max = min(self.current_display.shape[0], y_max)
        
        if x_max - x_min > 2 and y_max - y_min > 2:
            # Apply operation
            region = self.current_display[y_min:y_max, x_min:x_max]
            if self.mode == 'remove':
                self.current_display[y_min:y_max, x_min:x_max] = 0
            else:  # restore
                original_region = self.original_full[y_min:y_max, x_min:x_max]
                self.current_display[y_min:y_max, x_min:x_max] = original_region
            
            self.rectangles.append({
                'bounds': (x_min, y_min, x_max, y_max),
                'mode': self.mode
            })
            
            # Update display
            self.im2.set_data(self.current_display)
            self.fig.canvas.draw_idle()
        
        self.start_point = None
        if self.rect_artist:
            self.rect_artist.remove()
            self.rect_artist = None
    
    def on_motion(self, event):
        if not self.drawing or self.start_point is None or event.inaxes != self.ax2:
            return
        
        if self.rect_artist:
            self.rect_artist.remove()
        
        x1, y1 = self.start_point
        x2, y2 = int(event.xdata), int(event.ydata)
        
        width = x2 - x1
        height = y2 - y1
        
        from matplotlib.patches import Rectangle
        self.rect_artist = Rectangle((x1, y1), width, height, 
                                     fill=False, edgecolor='red', linewidth=2)
        self.ax2.add_patch(self.rect_artist)
        self.fig.canvas.draw_idle()
    
    def on_key(self, event):
        if event.key == 'r':
            self.mode = 'remove'
            print("Mode: REMOVE (click & drag to remove areas)")
        elif event.key == 's':
            self.mode = 'restore'
            print("Mode: RESTORE (click & drag to restore from original)")
        elif event.key == 'enter':
            self.result = self.current_display.copy()
            self.saved = True
            plt.close(self.fig)
            print("✓ Changes saved!")
        elif event.key == 'escape':
            self.result = self.cleaned.copy()
            self.saved = True
            plt.close(self.fig)
            print("✗ Changes cancelled. Using cleaned version.")
    
    def run(self):
        plt.show()
        if self.result is None:
            self.result = self.current_display.copy()
        return self.result


def main():
    print("=" * 60)
    print("EDGE ISLAND REMOVAL FILTER")
    print("=" * 60)
    
    # Phase 1: Load image
    print("\n[Phase 1] Loading image...")
    original = load_image(IMAGE_PATH)
    print(f"  Image shape: {original.shape}")
    print(f"  Image range: [{original.min()}, {original.max()}]")
    
    # Phase 2: Visualize tiles
    print("\n[Phase 2] Visualizing original tiles...")
    visualize_tiles(original, tile_size=TILE_SIZE, title="Original Image - Tile Breakdown")
    
    # Phase 3: Process image
    print("\n[Phase 3] Processing image (removing islands)...")
    cleaned, modified_tiles = process_image(original, tile_size=TILE_SIZE)
    print("  ✓ Image processing complete")
    
    # Phase 3b: Show modified tiles only
    print("\n[Phase 3b] Showing modified tiles...")
    display_modified_tiles(modified_tiles)
    
    # Phase 4: Display comparison and save
    print("\n[Phase 4] Displaying results and saving...")
    display_comparison(original, cleaned, tile_size=TILE_SIZE)
    
    # Phase 5: Interactive editor
    print("\n[Phase 5] Opening interactive editor...")
    print("  Controls:")
    print("    - Click & drag to select an area")
    print("    - 'R' key: Switch to REMOVE mode")
    print("    - 'S' key: Switch to RESTORE mode (bring back from original)")
    print("    - 'ENTER' key: Save changes")
    print("    - 'ESC' key: Cancel and use auto-cleaned version")
    
    editor = InteractiveImageEditor(original, cleaned, original)
    final_image = editor.run()
    
    # Save final image
    cv2.imwrite(OUTPUT_PATH, final_image)
    print(f"  ✓ Final image saved to: {OUTPUT_PATH}")
    
    # Calculate statistics
    original_white = np.sum(original > 0)
    final_white = np.sum(final_image > 0)
    removed_pixels = original_white - final_white
    print(f"\nStatistics:")
    print(f"  Original white pixels: {original_white}")
    print(f"  Final white pixels: {final_white}")
    print(f"  Pixels removed: {removed_pixels} ({100*removed_pixels/original_white:.1f}%)")
    print("\n✓ Processing complete!")


if __name__ == "__main__":
    main()

