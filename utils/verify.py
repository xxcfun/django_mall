"""
生成验证码：
1.准备素材
字体，文件内容，颜色，干扰线
2.画验证码
pip install Pillow , random
创建图片
记录文字内容， django session【服务器，python代码】
sdfsfs cookie 【浏览器】
（1）第一次请求，cookie + session 对应关系生成
（2）第二次请求，携带了cookie，找到对应的session【提交表单】
    请求带上验证码参数与session中的验证码进行比较
3. io文件流
BytesIO
"""
import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from django_mall import settings


class VerifyCode(object):
    """验证码类"""
    def __init__(self, dj_request):
        self.dj_request = dj_request
        # 验证码长度
        self.code_len = 4
        # 验证码图片尺寸
        self.img_width = 100
        self.img_height = 30
        # django中session的名称
        self.session_key = 'verify_code'

    def gen_code(self):
        """生成验证码"""
        # 1.使用随机数生成验证码字符串
        code = self._get_vcode()
        # 2.把验证码存在session中
        self.dj_request.session[self.session_key] = code
        # 3.准备随机元素（背景颜色、验证码文字的颜色、干扰线等）
        font_color = ['black', 'brown', 'red', 'darkblue', 'darkred', 'green', 'darkmagenta']
        # rbg随机背景颜色
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 字体路径
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesbi.ttf')

        # 创建图片
        im = Image.new('RGB', (self.img_width, self.img_height), bg_color)
        draw = ImageDraw.Draw(im)

        # 画干扰线
        # 随机条数，到底画几条
        for i in range(random.randrange(1, int(self.code_len / 2)) + 1):
            # 线条的颜色
            line_color = random.choice(font_color)
            # 线条的位置
            point = (
                random.randrange(0, self.img_width * 0.2),
                random.randrange(0, self.img_height),
                random.randrange(self.img_width - self.img_width * 0.2, self.img_width),
                random.randrange(0, self.img_height),
            )
            # 线条的宽度
            width = random.randrange(1, 4)
            draw.line(point, fill=line_color, width=width)

        # 画验证码
        for index, char in enumerate(code):
            code_color = random.choice(font_color)
            # 指定字体
            font_size = random.randrange(15, 25)
            font = ImageFont.truetype(font_path, font_size)
            point = (index * self.img_width / self.code_len,
                     random.randrange(0, self.img_height / 3))
            draw.text(point, char, font=font, fill=code_color)

        buf = BytesIO()
        im.save(buf, 'gif')
        return HttpResponse(buf.getvalue(), 'image/gif')


    def _get_vcode(self):
        random_str = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvb0123456789'
        code_list = random.sample(list(random_str), self.code_len)
        code = ''.join(code_list)
        return code

    def validate_code(self, code):
        """验证验证码是否正确"""
        # 1.转变大小写
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, '')
        return vcode.lower == code
