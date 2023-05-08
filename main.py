import keyboard
import pystray
from PIL import Image, ImageDraw
import time
import tkinter as tk
from tkinter import simpledialog
import os


def save_key_delay(delay):
    with open("key_delay.txt", "w") as f:
        f.write(str(delay))


def load_key_delay():
    if os.path.exists("key_delay.txt"):
        with open("key_delay.txt", "r") as f:
            delay = int(f.read().strip())
            return delay / 1000  # Convert ms to seconds
    return None


KEY_DELAY = load_key_delay() or 0.05  # Load the KEY_DELAY from the file, or use the default value (50ms)
last_key_time = {}  # Dictionary to store the last key press time for each key
key_state = {}  # Dictionary to store the state (pressed or released) of each key


def on_key_event(event):
    key = event.name  # Get the key name from the event
    now = time.time()  # Get the current time

    if event.event_type == 'up' and key_state.get(key, False):
        key_state[key] = False  # Update the key state to False (released)
        return True

    if key in last_key_time and now - last_key_time[key] < KEY_DELAY:
        return False

    last_key_time[key] = now
    key_state[key] = True
    return True


def create_key_icon():
    icon = Image.new('RGB', (16, 16), color='white')
    draw = ImageDraw.Draw(icon)

    draw.rectangle([(4, 4), (11, 11)], fill='black')
    draw.rectangle([(11, 6), (13, 8)], fill='black')
    draw.ellipse([(1, 1), (5, 5)], fill='black')

    return icon


def on_quit_action(icon, item):
    icon.stop()


def set_key_delay(icon, item):
    global KEY_DELAY
    root = tk.Tk()
    root.withdraw()
    delay = simpledialog.askinteger("Set KEY_DELAY", "Enter the KEY_DELAY in milliseconds:", minvalue=1, initialvalue=int(KEY_DELAY * 1000))
    if delay is not None:
        KEY_DELAY = delay / 1000  # Convert ms to seconds
        save_key_delay(delay)  # Save the KEY_DELAY to the file
    root.destroy()


# Add this function to your script
def save_key_icon(icon_path):
    key_icon = create_key_icon()
    key_icon.save(icon_path, format="ICO")


tray_icon = pystray.Icon("name", create_key_icon(), "Keyboard Double Click Fix")

menu = (
    pystray.MenuItem('Set KEY_DELAY...', set_key_delay),
    pystray.MenuItem('Quit', on_quit_action),
)
tray_icon.menu = menu

keyboard.hook(on_key_event, suppress=True)

icon_path = "key.ico"
save_key_icon(icon_path)

tray_icon.run()
