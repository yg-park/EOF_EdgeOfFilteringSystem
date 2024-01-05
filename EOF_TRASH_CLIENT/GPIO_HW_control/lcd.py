from RPLCD.i2c import CharLCD

class LCD:
	def __init__(self):
		self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
		self.lcd.clear()
	def display_lcd(self,display_type):
		if display_type == 'Pet':
			self.lcd.write_string('   Pet Bottle    Classification')
		elif display_type == 'Glass':
			self.lcd.write_string('  Glass Bottle   Classification')
		elif display_type == 'RCStart':
			self.lcd.write_string('    RC Start')
		elif display_type == 'RCStop':
			self.lcd.write_string('    RC Stop')
	def display_clear(self):
		self.lcd.clear()
myLCD = LCD()
myLCD.display_lcd('Glass')
