# Building a Windows 11 Uptime Tray Utility in Python

This lesson will guide you through creating a simple Windows 11 system tray utility in Python. The utility will display an icon in the system tray, and when you hover over it, it will show the current system uptime. The app will also start with Windows if you set it up to do so.

---

## Prerequisites

- **Python 3.7+** installed on your system.
- Basic familiarity with running Python scripts.

We will use the following Python packages:
- [`pystray`](https://github.com/moses-palmer/pystray): For creating the system tray icon.
- [`Pillow`](https://python-pillow.org/): For creating a simple icon image.
- [`psutil`](https://github.com/giampaolo/psutil): For retrieving system uptime.

### Install the required packages
Open a terminal or command prompt and run:

```sh
pip install pystray pillow psutil
```

---

## Step 1: Imports and Setup

First, import the necessary modules:

```python
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import psutil
import time
import threading
```

**What these do:**
- `pystray`: Handles the tray icon and its menu.
- `Pillow (PIL)`: Used to create a simple icon image.
- `psutil`: Lets us get the system uptime.
- `time` and `threading`: For updating the tooltip in the background.

---

## Step 2: Create a Simple Icon

We need an icon for our tray app. Let's create a simple one using Pillow:

```python
def create_image():
    # Create a simple black square icon with a white square inside
    image = Image.new('RGB', (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return image
```

**Explanation:**
- This function creates a 64x64 pixel black square with a smaller white square inside. You can customize this as you like.

---

## Step 3: Get System Uptime

We want to display how long the system has been running. `psutil` makes this easy:

```python
def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"Uptime: {hours}h {minutes}m {seconds}s"
```

**Explanation:**
- `psutil.boot_time()` returns the system boot time (in seconds since epoch).
- We subtract this from the current time to get uptime in seconds.
- We then convert seconds to hours, minutes, and seconds for readability.

---

## Step 4: Update the Tooltip Continuously

We want the tooltip to always show the current uptime. We'll use a background thread to update it every second:

```python
def update_tooltip(icon):
    while True:
        icon.title = get_uptime()
        time.sleep(1)  # Update every second
```

**Explanation:**
- This function runs in a loop, updating the tray icon's tooltip with the latest uptime every second.
- It runs in a separate thread so it doesn't block the main program.

---

## Step 5: Set Up the Tray Icon and Menu

Now, let's put it all together:

```python
def on_exit(icon, item):
    icon.stop()

def main():
    icon = pystray.Icon(
        "uptime",  # Unique name for the icon
        create_image(),  # The icon image
        "Uptime",  # Initial tooltip
        menu=pystray.Menu(
            item('Exit', on_exit)
        )
    )
    # Start the tooltip updater in a background thread
    threading.Thread(target=update_tooltip, args=(icon,), daemon=True).start()
    icon.run()
```

**Explanation:**
- `on_exit`: Stops the icon when you select 'Exit' from the tray menu.
- `main`: Sets up the tray icon, menu, and starts the background thread to update the tooltip.
- `icon.run()`: Starts the tray icon event loop.

---

## Step 6: Run the App

Add the standard Python entry point:

```python
if __name__ == "__main__":
    main()
```

---

## Full Code Listing

Here is the complete code in one file:

```python
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import psutil
import time
import threading

def create_image():
    image = Image.new('RGB', (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")
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
```

---

## Step 7: Make It Start with Windows (Optional)

To have your script start with Windows:
1. Press `Win + R`, type `shell:startup`, and press Enter. This opens the Startup folder.
2. Create a shortcut to your Python script in this folder. If you use a `.py` file, make sure Python is associated with `.py` files, or use `pythonw.exe` to avoid a console window.

**Tip:** You can also use [PyInstaller](https://pyinstaller.org/) to package your script as a standalone `.exe`.

---

## Summary
- You now have a Python system tray app that shows Windows uptime on hover!
- You can customize the icon and tooltip as you like.
- For more advanced features, explore the `pystray` and `psutil` documentation.

Happy coding! 