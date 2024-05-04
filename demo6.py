import input_chinese
oled_controller = input_chinese.OLEDController()#创建实例
oled_controller.display_chinese_on_oled("你好word",0,20) #后面的为显示位置
# # 创建OLED控制器实例，并指定SCL和SDA引脚
# oled_controller = OLEDController(scl_pin=22, sda_pin=21)

# # 调用显示中文字符的方法
# oled_controller.display_chinese_on_oled("你好世界！")
