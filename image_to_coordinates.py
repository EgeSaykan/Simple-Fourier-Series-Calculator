from PIL import Image
import os

def extract_white_pixels(image_path, output_path, white_threshold=250):
    """
    Extract white pixel coordinates from an image and save to a file.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the coordinates
        white_threshold: Minimum RGB value to consider a pixel white (default: 250)
    """
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
    
    # Open image and convert to RGB (handles different formats/modes)
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    
    width, height = img.size
    print(f"Image size: {width}x{height}")
    
    # Extract white pixel coordinates
    white_pixels = []
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]  # Get RGB values
            # Check if pixel is white (all channels above threshold)
            if r >= white_threshold and g >= white_threshold and b >= white_threshold:
                white_pixels.append((x, y))
    
    print(f"Found {len(white_pixels)} white pixels")
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write coordinates to file
    try:
        with open(output_path, 'w') as f:
            for x, y in white_pixels:
                f.write(f"{x} {y}\n")
        print(f"Coordinates saved to {output_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        return

if __name__ == "__main__":
    # Configuration
    image_path = "image_cleaned.jpg"
    output_path = "txtfiles/points.txt"
    
    extract_white_pixels(image_path, output_path)
