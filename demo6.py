import input_chinese
oled_controller = input_chinese.OLEDController()#创建实例
oled_controller.display_chinese_on_oled("你好word",0,20) #后面的为显示位置
# # 创建OLED控制器实例，并指定SCL和SDA引脚,font_size为更改字体大小,建议为双数这样才能显示正常，默认大小为 2  以上内容没有更改的需要可以不填
# oled_controller = OLEDController(scl_pin=22, sda_pin=21, font_size=2)

# # 调用显示中文字符的方法
# oled_controller.display_chinese_on_oled("你好世界！")
