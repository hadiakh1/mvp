"""
Script to make the logo background transparent while preserving colors.
"""
from PIL import Image
import os

def make_background_transparent(image_path, output_path=None, threshold=240):
    """
    Make white/light background transparent while preserving logo colors.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the output (defaults to overwriting input)
        threshold: RGB threshold for considering a pixel as background (0-255)
    """
    # Open the image
    img = Image.open(image_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get image data
    data = img.getdata()
    
    # Create new image data with transparent background
    new_data = []
    for item in data:
        # If pixel is white/light (above threshold), make it transparent
        # Check if it's close to white (all RGB values high)
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            # Make transparent
            new_data.append((255, 255, 255, 0))
        else:
            # Keep original color with full opacity
            new_data.append(item)
    
    # Update image data
    img.putdata(new_data)
    
    # Save the image
    if output_path is None:
        output_path = image_path
    
    img.save(output_path, "PNG")
    print(f"Logo processed and saved to {output_path}")
    print("Background made transparent while preserving logo colors.")


if __name__ == "__main__":
    # Get the logo path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "static", "logo.png")
    
    if not os.path.exists(logo_path):
        print(f"Error: Logo not found at {logo_path}")
        exit(1)
    
    try:
        # Make background transparent (using threshold of 240 for white/light backgrounds)
        make_background_transparent(logo_path, threshold=240)
        print("\n✓ Logo background successfully made transparent!")
    except ImportError:
        print("Error: Pillow (PIL) is required.")
        print("Install it with: pip install Pillow")
    except Exception as e:
        print(f"Error processing logo: {e}")
        import traceback
        traceback.print_exc()

