"""
Generate placeholder profile images for sample lawyers.
This creates simple colored circular avatars with initials.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Colors for different lawyers
COLORS = [
    ("#3B82F6", "#1E40AF"),  # Blue
    ("#10B981", "#047857"),  # Green
    ("#F59E0B", "#D97706"),  # Amber
    ("#EF4444", "#DC2626"),  # Red
    ("#8B5CF6", "#7C3AED"),  # Purple
    ("#EC4899", "#DB2777"),  # Pink
    ("#06B6D4", "#0891B2"),  # Cyan
    ("#F97316", "#EA580C"),  # Orange
    ("#6366F1", "#4F46E5"),  # Indigo
    ("#14B8A6", "#0D9488"),  # Teal
    ("#F43F5E", "#E11D48"),  # Rose
    ("#84CC16", "#65A30D"),  # Lime
]

INITIALS = [
    "SM", "MC", "ER", "DT", "JP", "RW",
    "LA", "JM", "AF", "CL", "PB", "DT"
]

def create_profile_image(filename, initials, color_pair, index):
    """Create a circular profile image with initials."""
    size = 200
    bg_color, text_color = color_pair
    
    # Create image with transparent background
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    margin = 10
    draw.ellipse([margin, margin, size-margin, size-margin], fill=bg_color, outline=text_color, width=3)
    
    # Try to use a font, fallback to default if not available
    try:
        font_size = 60
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    
    # Draw text
    draw.text(position, initials, fill=text_color, font=font)
    
    # Save image
    img.save(filename, "PNG")
    print(f"Created {filename}")


def main():
    """Generate all profile images."""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    
    for i in range(12):
        filename = os.path.join(static_dir, f"lawyer{i+1}.jpg")
        initials = INITIALS[i]
        color = COLORS[i % len(COLORS)]
        create_profile_image(filename, initials, color, i)
    
    # Also create a default avatar
    default_file = os.path.join(static_dir, "default-avatar.png")
    create_profile_image(default_file, "LA", ("#6B7280", "#374151"), 0)
    print("\nAll profile images generated!")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Pillow (PIL) is required to generate images.")
        print("Install it with: pip install Pillow")
        print("\nAlternatively, you can use placeholder images from a service like:")
        print("https://ui-avatars.com/api/?name=Lawyer+Name&size=200&background=random")

