import binascii
import gb2312
import framebuf
from machine import Pin, I2C
import ssd1306

class OLEDController:
    def __init__(self, scl_pin=22, sda_pin=21):
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.i2c = I2C(0, scl=Pin(self.scl_pin), sda=Pin(self.sda_pin))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.buf = bytearray(128 * 64 // 8)
        self.fb = framebuf.FrameBuffer(self.buf, 128, 64, framebuf.MONO_HLSB)
        self.KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
        self.rect_list = [[] for _ in range(16)]
        self.font_file = "HZK16"

    def hex_to_bytes(self, hex_string):
        if len(hex_string) % 2 != 0:
            raise ValueError("Hex string length must be even.")
        byte_array = bytearray()
        for i in range(0, len(hex_string), 2):
            byte = int(hex_string[i:i+2], 16)
            byte_array.append(byte)
        return bytes(byte_array)

    def display_char(self, char, x, y):
        # 清除原来的内容
        #self.fb.fill(0)  # 清除帧缓冲区内容

        try:
            self.display_chinese(char, x, y)
        except:
            self.fb.text(char, x, y)

        self.oled.blit(self.fb, 0, 0)  # 将framebuf内容显示到OLED屏幕上
        self.oled.show()  # 更新显示

    def display_chinese(self, char, x, y):
        self.rect_list = [[] for _ in range(16)]  # 清空绘制列表

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

        for row in range(len(self.rect_list)):
            for col in range(len(self.rect_list[0])):
                if self.rect_list[row][col]:
                    self.fb.pixel(col+x, row+y, 1)  # 在帧缓冲区中设置一个白色像素

    def display_chinese_on_oled(self, text, x=0, y=0):
        for index, char in enumerate(text):
            self.display_char(char, x + index * 16, y)
        #self.oled.show()

# 创建OLED控制器实例
oled_controller = OLEDController()

# 调用示例
#oled_controller.display_chinese_on_oled("red", 0, 0)



