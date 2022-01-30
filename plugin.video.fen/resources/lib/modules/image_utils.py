# -*- coding: utf-8 -*-
import colorsys
from PIL import ImageFilter, Image
import sqlite3 as database
from modules.kodi_utils import translate_path
# from modules.kodi_utils import logger

# ImageColors code from Jurial, Sualfred, likely Phil65 originally as well.
# Heavily edited for Fen.

kodi_texture_db = translate_path('special://database/Textures13.db')
rgb_list = [None, None, None]
brightness_threshold = 0.2
darkness_threshold = 0.6
max_dark_adjustment = 2
max_bright_adjustment = 1
brightness_compare = 0.39

class ImageColors:
	def run(self, source):
		img = self.open_image(source)
		maincolor_rgb = self.get_maincolor(img)
		maincolor_hex = self.rgb_to_hex(*self.get_color_lumsat(*maincolor_rgb))
		img.close()
		return maincolor_hex, self.brightness

	def open_image(self, source):
		img = Image.open(source)
		img.thumbnail((200, 200), Image.ANTIALIAS)
		img = img.convert('RGB')
		return img

	def clamp(self, x):
		return max(0, min(x, 255))

	def rgb_to_int(self, r, g, b):
		return [int(self.clamp(i * 255)) for i in [r, g, b]]

	def rgb_to_hex(self, r, g, b):
		return 'FF%02x%02x%02x' % (r, g, b)

	def get_maincolor(self, img):
		for channel in range(3):
			pixels = img.getdata(band=channel)
			values = [pixel for pixel in pixels]
			rgb_list[channel] = self.clamp(sum(values) / len(values))
		return rgb_list

	def get_color_lumsat(self, r, g, b):
		hue, lum, sat = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
		self.lum, self.brightness = self.check_brightness(lum)
		return self.rgb_to_int(*colorsys.hls_to_rgb(hue, self.lum, sat))

	def check_brightness(self, lum):
		brightness = round(lum, 2)
		if brightness <= brightness_threshold: multiplier = min(1 + (brightness_threshold - brightness)/float(lum), max_dark_adjustment)
		elif brightness >= darkness_threshold: multiplier = 1 - min((brightness - darkness_threshold)/float(brightness), max_bright_adjustment)
		else: multiplier = 1.00
		lum *= multiplier
		return lum, (brightness >= brightness_compare)

def fetch_kodi_imagecache(poster):
	image = None
	dbcon = database.connect(kodi_texture_db)
	dbcur = dbcon.cursor()
	dbcur.execute("SELECT cachedurl FROM texture WHERE url = ?", (poster,))
	try: image = dbcur.fetchone()[0]
	except: pass
	dbcon.close()
	return image
