import binascii
import gb2312
import framebuf
from machine import Pin, I2C
import ssd1306

# 设置I2C总线
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# 设置SSD1306 OLED显示器
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 创建1位深度的framebuf
buf = bytearray(128 * 64 // 8)
fb = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB)

# 字节码常量
KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

# 初始化16*16的点阵位置
rect_list = [[] for _ in range(16)]

def hex_to_bytes(hex_string):
    if len(hex_string) % 2 != 0:
        raise ValueError("Hex string length must be even.")
    byte_array = bytearray()
    for i in range(0, len(hex_string), 2):
        byte = int(hex_string[i:i+2], 16)
        byte_array.append(byte)
    return bytes(byte_array)

def display_chinese_on_oled(text):
    for char in text:
        display_chinese(char)

    oled.fill(0)  # 清空OLED显示器
    for row in range(len(rect_list)):
        for col in range(len(rect_list[0])):
            if rect_list[row][col]:
                fb.pixel(col, row, 1)  # 在帧缓冲区中设置一个白色像素
    oled.blit(fb, 0, 0)  # 将framebuf内容显示到OLED屏幕上
    oled.show()  # 更新显示

def display_chinese(char):
    get_gb2312 = gb2312.fontbyte.strs(char)
    hex_str = binascii.hexlify(get_gb2312).decode('utf-8')
    area = eval('0x' + hex_str[:2]) - 0xA0
    index = eval('0x' + hex_str[2:]) - 0xA0
    offset = (94 * (area-1) + (index-1)) * 32

    font_rect = None
    with open("HZK16", "rb") as f:
        f.seek(offset)
        font_rect = f.read(32)

    for k in range(len(font_rect) // 2):
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                flag = asc & KEYS[i]
                row_list.append(flag)

# 调用示例
display_chinese_on_oled("你好世界！")

