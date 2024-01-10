"""
I2C LCD를 제어하는 모듈입니다.
"""
from RPLCD.i2c import CharLCD


class LCD:
    """I2C LCD를 제어하기 위한 클래스입니다."""
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x27, port=1,
            cols=16, rows=2, dotsize=8
        )
        self.lcd.clear()

    def display_lcd(self, display_type):
        """LCD에 문자열을 출력합니다."""
        self.lcd.clear()
        if display_type == 'Pet':
            self.lcd.write_string('   Pet Bottle    Classification')
        elif display_type == 'Glass':
            self.lcd.write_string('  Glass Bottle   Classification')
        elif display_type == 'RCStart':
            self.lcd.write_string('    RC Start')
        elif display_type == 'RCStop':
            self.lcd.write_string('    RC Stop')
        else:
            self.lcd.write_string(display_type)
