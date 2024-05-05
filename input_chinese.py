import binascii
import gb2312
import framebuf
from machine import Pin, I2C
import ssd1306

class OLEDController:
    def __init__(self, scl_pin=22, sda_pin=21, font_size=2):
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.font_size = font_size  # 添加字体大小变量
        self.i2c = I2C(0, scl=Pin(self.scl_pin), sda=Pin(self.sda_pin))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.buf = bytearray(128 * 64 // 8)
        self.fb = framebuf.FrameBuffer(self.buf, 128, 64, framebuf.MONO_HLSB)
        self.KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
        self.rect_list = [[] for _ in range(16)]
        self.font_file = "HZK16"

    def display_char(self, char, x, y):
        try:
            self.display_chinese(char, x, y)
        except:
            self.fb.text(char, x, y)

        self.oled.blit(self.fb, 0, 0)
        self.oled.show()

    def display_chinese(self, char, x, y):
        self.rect_list = [[] for _ in range(16)]

        get_gb2312 = gb2312.fontbyte.strs(char)
        hex_str = binascii.hexlify(get_gb2312).decode('utf-8')
        area = eval('0x' + hex_str[:2]) - 0xA0
        index = eval('0x' + hex_str[2:]) - 0xA0
        offset = (94 * (area-1) + (index-1)) * 32

        font_rect = None
        with open(self.font_file, "rb") as f:
            f.seek(offset)
            font_rect = f.read(32)

        for k in range(len(font_rect) // 2):
            row_list = self.rect_list[k]
            for j in range(2):
                for i in range(8):
                    asc = font_rect[k * 2 + j]
                    flag = asc & self.KEYS[i]
                    row_list.append(flag)

        # 计算新的字体大小
        new_font_size = self.font_size // 2
        for row in range(len(self.rect_list)):
            for col in range(len(self.rect_list[0])):
                if self.rect_list[row][col]:
                    self.fb.fill_rect(x + col * new_font_size, y + row * new_font_size, new_font_size, new_font_size, 1)

    def display_chinese_on_oled(self, text, x=0, y=0):
        for index, char in enumerate(text):
            self.display_char(char, x + index * self.font_size*8, y)


# 创建 OLED 控制器实例
oled_controller = OLEDController()

# 调用示例
#oled_controller.display_chinese_on_oled("你好世界word", 0, 0)

