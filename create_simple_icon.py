import os
from PIL import Image, ImageDraw, ImageFont

def create_2048_icon():
    """Create a simple, clean 2048 game icon"""
    
    # Create a new image with RGBA mode
    icon_size = 256
    img = Image.new('RGBA', (icon_size, icon_size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    tile_color = (237, 194, 46)  # Golden/yellow for 2048 tile
    text_color = (255, 255, 255)  # White text
    
    # Create a square with rounded corners for the tile
    padding = 20
    tile_size = icon_size - (padding * 2)
    
    # Draw the main square
    draw.rectangle(
        [padding, padding, padding + tile_size, padding + tile_size],
        fill=tile_color
    )
    
    # Try to add "2048" text
    try:
        # Try to find a font
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            # Fallback to default
            font = ImageFont.load_default()
        
        # Add the text "2048" centered
        text = "2048"
        text_width = draw.textlength(text, font=font)
        text_height = 80  # Approximation
        
        text_x = (icon_size - text_width) // 2
        text_y = (icon_size - text_height) // 2
        
        draw.text((text_x, text_y), text, fill=text_color, font=font)
    except Exception as e:
        print(f"Couldn't add text: {e}")
        # Draw simple text if fancy text fails
        draw.text((80, 100), "2048", fill=text_color)
    
    # Ensure assets directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Save as PNG first
    png_path = os.path.join(assets_dir, "2048_icon.png")
    img.save(png_path, "PNG")
    print(f"PNG icon saved to {png_path}")
    
    # Convert to ICO
    ico_path = os.path.join(assets_dir, "2048_icon.ico")
    
    # Create different sizes for the icon
    sizes = [16, 32, 48, 64, 128, 256]
    img_list = []
    
    for size in sizes:
        resized_img = img.resize((size, size), Image.LANCZOS)
        img_list.append(resized_img)
    
    # Save as ICO
    img.save(
        ico_path,
        format='ICO',
        sizes=[(i.width, i.height) for i in img_list]
    )
    
    print(f"ICO icon saved to {ico_path}")
    return ico_path

if __name__ == "__main__":
    try:
        path = create_2048_icon()
        print(f"Successfully created icon at: {path}")
    except Exception as e:
        print(f"Error creating icon: {e}")
        import traceback
        traceback.print_exc() 