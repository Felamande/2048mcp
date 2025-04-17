import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_2048_icon():
    # Create a new image with transparent background
    icon_size = 256
    img = Image.new('RGBA', (icon_size, icon_size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw the tile with rounded corners
    tile_size = icon_size - 40
    tile_color = (237, 194, 46)  # 2048 tile color (gold)
    
    # Fill background with rounded rectangle
    # Since rounded corners are tricky, we'll draw a filled rectangle and then add rounded corners
    draw.rectangle(
        [20, 20, 20 + tile_size, 20 + tile_size],
        fill=tile_color
    )
    
    # Draw the "2048" text
    text = "2048"
    
    # Try to use a bold font for the text
    try:
        # Try Arial Bold if available
        font = ImageFont.truetype("arialbd.ttf", 80)
    except:
        try:
            # Fallback to any available system font
            font = ImageFont.load_default().font_variant(size=70)
        except:
            font = None

    # Calculate text position to center it
    if font:
        text_width = draw.textlength(text, font=font)
        text_height = 80  # Approximate height based on font size
        text_x = (icon_size - text_width) // 2
        text_y = (icon_size - text_height) // 2
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    else:
        # Simple fallback if no font is available
        draw.text((80, 100), text, fill=(255, 255, 255))
    
    # Make sure assets directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Save as PNG first to verify image
    png_path = os.path.join(assets_dir, "2048_icon.png")
    img.save(png_path, "PNG")
    print(f"PNG icon saved to {png_path}")
    
    # Save as ICO with multiple sizes
    icon_path = os.path.join(assets_dir, "2048_icon.ico")
    
    # Create different sizes for the icon
    sizes = [16, 32, 48, 64, 128, 256]
    img_list = []
    
    for size in sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        img_list.append(resized_img)
    
    # Save as ICO
    img_list[0].save(
        icon_path,
        format='ICO',
        sizes=[(i.width, i.height) for i in img_list]
    )
    
    print(f"ICO icon saved to {icon_path}")
    return icon_path

if __name__ == "__main__":
    try:
        path = create_2048_icon()
        print(f"Successfully created icon at: {path}")
    except Exception as e:
        print(f"Error creating icon: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 