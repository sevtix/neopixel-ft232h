from __future__ import division

# script by Severin Schmid [ sevtixdev@gmail.com ]

# ---- OPTIONS ---- #

speed = 5
stretching = 0.01
lenght = 50

# ---- OPTIONS ---- #

# ---- GAMMA CORRECTION ---- #
gamma = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]
# ---- GAMMA CORRECTION ---- #


import time
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H
import colorsys

millis = lambda: int(round(time.time() * 1000))

class NeoPixel_FT232H(object):
	def __init__(self, n):
		self.ft232h = FT232H.FT232H()
		self.spi    = FT232H.SPI(self.ft232h, max_speed_hz=8000000)
		self.buffer = bytearray(n*24)
		self.lookup = self.build_byte_lookup()

	def build_byte_lookup(self):
		lookup = {}
		for i in range(256):
			value = bytearray()
			for j in range(7, -1, -1):
				if ((i >> j) & 1) == 0:
					value.append(0b11100000)
				else:
					value.append(0b11111000)
			lookup[i] = value
		return lookup

	def set_pixel_color(self, n, r, g, b):
		index = n*24
		self.buffer[index   :index+8 ] = self.lookup[int(g)]
		self.buffer[index+8 :index+16] = self.lookup[int(r)]
		self.buffer[index+16:index+24] = self.lookup[int(b)]

	def show(self):
		self.spi.write(self.buffer)


def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def rainbow(pixels, pixel_count, spacing, hsv):
				hsvranged = hsv / 255
				offset = 0.0
				for pix in range(pixel_count):
					if (hsvranged + offset <= 1) :
						r,g,b = hsv2rgb(hsvranged + offset, 1, 1)
					else:
						r,g,b = hsv2rgb(hsvranged + offset - 1, 1, 1)
					#pixels.set_pixel_color(pix, r, g, b)
					pixels.set_pixel_color(pix, gamma[int(r)], gamma[int(g)], gamma[int(b)])
					offset = offset + spacing
				pixels.show()
				time.sleep(0.0025)

if __name__ == '__main__':
	pixels = NeoPixel_FT232H(lenght)
	pixels.show()
	timestamp = millis()
	hsv = 0
	while True:

		if((millis() - timestamp) >= speed):
			rainbow(pixels, lenght, stretching, hsv)
			timestamp = millis()
			if(hsv == 255):
				hsv = 0
			else:
				hsv = hsv + 1
