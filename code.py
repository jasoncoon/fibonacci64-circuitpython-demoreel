# Fibonacci64 - Demo Reel - CircuitPython & NeoPixel
# https://gist.github.com/jasoncoon/6884626781bac0f922c48d2a406a8a57
# https://www.evilgeniuslabs.org/fibonacci64-micro

# This example uses CircuitPython and the Adafruit NeoPixel library
# You'll need neopixel.mpy in your /lib directory
# More information: https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries

import adafruit_fancyled.adafruit_fancyled as fancy
import adafruit_fancyled.fastled_helpers as helper
import board
import neopixel
import time

from palettes import palette_count, palettes
from maps import radii, angles, coords_x, coords_y

pixel_pin = board.D10
num_pixels = 64
seconds_per_pattern = 10

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    brightness=0.0625,
    auto_write=False)

# index of the current palette, we'll increment this periodically with a timer
palette_index = 0

# timer used to increment the palette index
next_palette_time = time.monotonic() + 5

# timer used to blend the current palette to the next
blend_palette_time = time.monotonic() + 0.04

current_palette = palettes[palette_index].copy()
target_palette = palettes[palette_index]

hue = 0


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def next_palette():
    """ Increment the palette index and reset the timer """
    global palette_index
    global target_palette
    global next_palette_time

    # print('next_palette')
    palette_index = (palette_index + 1) % palette_count
    target_palette = palettes[palette_index]

    next_palette_time = time.monotonic() + 5


def blend_palettes(current, target, weight):
    for i in range(len(current)):
        current[i] = fancy.mix(current[i], target[i], weight)


def blend_current_palette():
    """ Blend the palettes and reset the timer """
    global palette_index
    global target_palette
    global current_palette
    global blend_palette_time

    # print('blend_palettes')
    blend_palettes(current_palette, target_palette, 0.01)

    blend_palette_time = time.monotonic() + 0.04


def rainbow_radius():
    global hue
    for i in range(num_pixels):
        h = (radii[i] * 4 + hue) % 255
        pixels[i] = fancy.CHSV(h, 255, 255).pack()
    hue = (hue - 4) % 255

def rainbow_angle():
    global hue
    for i in range(num_pixels):
        h = (angles[i] + hue) % 255
        pixels[i] = fancy.CHSV(h, 255, 255).pack()
    hue = (hue - 4) % 255


def rainbow_x():
    global hue
    for i in range(num_pixels):
        h = (coords_x[i] + hue) % 255
        pixels[i] = fancy.CHSV(h, 255, 255).pack()
    hue = (hue - 4) % 255


def rainbow_y():
    global hue
    for i in range(num_pixels):
        h = (coords_y[i] + hue) % 255
        pixels[i] = fancy.CHSV(h, 255, 255).pack()
    hue = (hue - 4) % 255


def rainbow_xy():
    global hue
    for i in range(num_pixels):
        h = (coords_x[i] + coords_y[i] + hue) % 255
        pixels[i] = fancy.CHSV(h, 255, 255).pack()
    hue = (hue - 4) % 255


def palette_radius():
    global hue
    global target_palette

    for i in range(num_pixels):
        radius = radii[i]
        color = helper.ColorFromPalette(current_palette, radius - hue)
        pixels[i] = color.pack()
    hue = (hue - 4) % 255


def palette_angle():
    global hue
    global target_palette

    for i in range(num_pixels):
        radius = angles[i]
        color = helper.ColorFromPalette(current_palette, radius - hue)
        pixels[i] = color.pack()


def palette_x():
    global hue
    global target_palette

    for i in range(num_pixels):
        radius = coords_x[i]
        color = helper.ColorFromPalette(current_palette, radius - hue)
        pixels[i] = color.pack()


def palette_y():
    global hue
    global target_palette

    for i in range(num_pixels):
        radius = coords_y[i]
        color = helper.ColorFromPalette(current_palette, radius - hue)
        pixels[i] = color.pack()


def palette_xy():
    global hue
    global target_palette

    for i in range(num_pixels):
        radius = coords_x[i] + coords_y[i]
        color = helper.ColorFromPalette(current_palette, radius - hue)
        pixels[i] = color.pack()
    
    
patterns = [
    palette_radius,
    palette_angle,
    palette_x,
    palette_y,
    palette_xy,
    rainbow_radius,
    rainbow_angle,
    rainbow_x,
    rainbow_y,
    rainbow_xy
]

pattern_count = len(patterns)

pattern_index = 0

# timer used to increment the pattern index
next_pattern_time = time.monotonic() + seconds_per_pattern

while True:
    patterns[pattern_index]()
    
    pixels.show()
    
    # time.sleep(.04)    

    if time.monotonic() > next_palette_time:
        next_palette()

    if time.monotonic() > blend_palette_time:
        blend_current_palette()
        
    if time.monotonic() > next_pattern_time:
        pattern_index = (pattern_index + 1) % pattern_count
        # if pattern_index >= pattern_count: pattern_index = 0
        next_pattern_time = time.monotonic() + seconds_per_pattern