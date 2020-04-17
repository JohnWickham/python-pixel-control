import board
import neopixel
import time
import argparse
from pixelProvider import SolidColorPixelProvider, RainbowPixelProvider

# Read arguments from the command line

argparser = argparse.ArgumentParser(description='Manipulate NeoPixel lighting hardware by writing out color and brightness data.')

color_group = argparser.add_mutually_exclusive_group(required=True)
color_group.add_argument('-c', '--color', type=int, nargs=4, metavar=('red', 'green', 'blue', 'white'))
color_group.add_argument('-p', '--preset', type=str, choices=['red', 'orange', 'yellow', 'green', 'blue', 'pink', 'purple', 'cyan', 'white', 'warm-white', 'cool-white', 'rainbow', 'off'], help='Named color preset to apply.')
argparser.add_argument('-b', '--brightness', type=float, default=1.0, help='Brightness level to set the pixel set to. Between 0.0 and 1.0.')
argparser.add_argument('-n', '--number', type=int, default=24, metavar='number', help='Number of pixels in the set.')
argparser.add_argument('-t', '--transition', type=str, choices=['fade-in', 'sequence', 'sequence-reverse'], help='Animation to use when applying this color to the pixel set.')
argparser.add_argument('-a', '--animation', type=str, choices=['breathe', 'fade-in-out', 'pulse-fade-in', 'pulse-fade-out', 'flash'], help='Repeating animation to run on the pixel set.')

args = argparser.parse_args()

# Define pixel constants
pixel_pin = board.D12
num_pixels = args.number
brightness = args.brightness

# Initialize the pixel set
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=neopixel.GRBW)

# MARK: Set the color

provider = None

presets = {
    'red': SolidColorPixelProvider((255, 0, 0, 0)),
    'orange': SolidColorPixelProvider((205, 30, 0, 0)),
    'yellow': SolidColorPixelProvider((200, 100, 0, 0)),
    'green': SolidColorPixelProvider((0, 255, 0, 0)),
    'blue': SolidColorPixelProvider((0, 0, 255, 0)),
    'pink': SolidColorPixelProvider((255, 50, 50, 0)),
    'purple': SolidColorPixelProvider((255, 0, 255, 0)),
    'cyan': SolidColorPixelProvider((0, 255, 255, 0)),
    'white': SolidColorPixelProvider((255, 255, 255, 255)),
    'warm-white': SolidColorPixelProvider((0, 0, 0, 255)),
    'cool-white': SolidColorPixelProvider((0, 0, 255, 255)),
    'rainbow': RainbowPixelProvider(num_pixels),
    'off': SolidColorPixelProvider((0, 0, 0, 0))
}

if args.preset is not None:
    provider = presets[args.preset]
elif args.color is not None:
    red = args.color[0]
    green = args.color[1]
    blue = args.color[2]
    white = args.color[3]
    provider = SolidColorPixelProvider((red, green, blue, white))

def set_brightness(level):
    global brightness
    brightness = level
    pixels.brightness = brightness

# Limit brightness if the requested color will draw too much power.
#   Each diode in a pixel will draw ~20mA at full brightness, 80mA in total.
#   Cap power draw at 60mA per pixel.s
pixelValueSum = 0
for i in range(num_pixels):
    pixelValue = provider.pixel_color(i)
    pixelValueSum += sum(pixelValue)

if pixelValueSum > 756 and (brightness is not None and brightness > 0.75):
    set_brightness(0.75) # TODO: Calculate the maximum brightness we can retain while staying below 60mA, instead of fixing it at 75%.

# Animations

# Transition Animations
#   Note when defining animations that the pixels will always clear before starting the animation because a new pixel set is initialized each time this script is run.

def fillPixels():
    for i in range(num_pixels):
        pixels[i] = provider.pixel_color(i)
    pixels.show()

def fade_to(level, speed=0.01):
    global brightness
    if level > brightness:
        while level > brightness:
            set_brightness(brightness + 0.01)
            pixels.show()
            time.sleep(speed)
    else:
        while level < brightness:
            set_brightness(brightness - 0.01)
            pixels.show()
            time.sleep(speed)

def fill_sequential(reverse=False):
    delay = (0.5 / num_pixels)
    
    pixelRange = range(num_pixels) 
    if reverse == True:
        pixelRange = range(num_pixels - 1, -1, -1)
   
    for i in pixelRange:
        pixels[i] = provider.pixel_color(i)
        pixels.show()
        time.sleep(delay)

def fill_fade_in(duration):
    target_brightness = brightness
    set_brightness(0.0)
    fillPixels()
    fade_to(target_brightness)

if args.transition is not None:
    if args.transition == 'sequence':
        fill_sequential()
    elif args.transition == 'sequence-reverse':
        fill_sequential(reverse=True)
    elif args.transition == 'fade-in':
        fill_fade_in(0.5)
else:
    fillPixels()

# Repeating Animations

def fade_in_out():
    while True:
        fade_to(0.0)
        fade_to(1.0)
        time.sleep(1)

def pulse_fade_out():
    while True:
        fade_to(0.0)
        set_brightness(1.0)

def pulse_fade_in():
    while True:
        fade_to(1.0)
        set_brightness(0.0)

def breathe():
    while True:
        fade_to(0.0, 0.03)
        time.sleep(2)
        fade_to(0.8, 0.03)
        time.sleep(0.4)

def flash():
    while True:
        pixels.fill((0, 0, 0, 0))
        time.sleep(0.5)
        fillPixels()
        time.sleep(0.5)

if args.animation is not None:
    if args.animation == 'breathe':
        breathe()
    elif args.animation == 'fade-in-out':
        fade_in_out()
    elif args.animation == 'pulse-fade-out':
        pulse_fade_out()
    elif args.animation == 'pulse-fade-in':
        pulse_fade_in()
    elif args.animation == 'flash':
        flash()