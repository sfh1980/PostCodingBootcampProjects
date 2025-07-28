import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import psutil
import time
import threading

def create_image():
    # Increase icon size for better visibility
    icon_size = 128  # Increased from 64 to 128
    image = Image.new('RGB', (icon_size, icon_size), "white")
    draw = ImageDraw.Draw(image)
    text = "Up"
    font_size = 92  # Increased from 32 to 72
    
    # Try multiple font options for better compatibility
    font = None
    font_options = [
        "arial.ttf",
        "arial.ttc", 
        "segoeui.ttf",
        "calibri.ttf",
        "tahoma.ttf"
    ]
    
    try:
        from PIL import ImageFont
        for font_name in font_options:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
    except:
        pass
    
    # If no TrueType font found, use default with larger size
    if font is None:
        try:
            font = ImageFont.load_default()
            # Scale up the default font
            font_size = 48  # Adjust for default font
        except:
            font = None
    
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
    else:
        bbox = draw.textbbox((0, 0), text)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((icon_size - text_width) // 2, (icon_size - text_height) // 2)
    draw.text(position, text, fill="black", font=font)
    
    # Resize to standard system tray size (Windows typically uses 16x16 or 32x32)
    # But we'll keep it larger for better visibility
    final_size = 64  # Good balance between visibility and system tray compatibility
    image = image.resize((final_size, final_size), Image.Resampling.LANCZOS)
    
    return image

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"Uptime: {hours}h {minutes}m {seconds}s"

def update_tooltip(icon):
    while True:
        icon.title = get_uptime()
        time.sleep(1)
        
def on_exit(icon, item):
    icon.stop()
    
def main():
    icon = pystray.Icon(
        "uptime",
        create_image(),
        "Uptime",
        menu=pystray.Menu(
            item('Exit', on_exit)
        )
    )
    threading.Thread(target=update_tooltip, args=(icon,), daemon=True).start()
    icon.run()
    
if __name__ == "__main__":
    main()