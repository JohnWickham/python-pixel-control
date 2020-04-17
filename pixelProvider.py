from abc import ABC;

class PixelProvider(ABC):
    
    def pixel_color(self, index):
        pass
        
class SolidColorPixelProvider(PixelProvider):

    color = (0, 0, 0, 0)

    def __init__(self, color):
        self.color = color

    def pixel_color(self, index):
        return self.color

class RainbowPixelProvider(PixelProvider):

    pixelCount = 0

    def __init__(self, pixelCount):
        self.pixelCount = pixelCount

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3, 0)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3, 0)

    def pixel_color(self, index):
        for j in range(255):
            rc_index = (index * 256 // self.pixelCount) + j
            color = self.wheel(rc_index & 255)
            return color