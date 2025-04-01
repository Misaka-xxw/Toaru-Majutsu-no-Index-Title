"""
File: titleGenerator.py
Description: 生成带有渐变蒙版的魔禁风格字体图片
Author: Misaka-xxw
Created: 2025-03-30
"""
import math
from enum import Enum

from PIL import Image, ImageDraw, ImageFont

from resource_path import resource_path


class BgType(Enum):
    """背景类型"""
    ALPHA = 1  # 透明背景
    SOLID = 2  # 纯色背景
    PICTURE = 3  # 图片背景


class TextType(Enum):
    """字体描边类型"""
    ALPHA = 1  # 方框里的字透明
    WHITE = 2  # 方框里的字填上白色
    HARD_OUTFIT = 3  # 方框里的字填上白色，然后再描边一圈
    SOFT_OUTFIT = 4  # 方框里的字填上白色，然后再描边一圈，但是描边的是柔和的
    # METAL = 5  # 金属质感，不会做，等pr救救


class Direction(Enum):
    """字体排列方向"""
    HORIZONTAL = 1  # 水平
    VERTICAL = 2  # 垂直


def generate_font_image(text1: str = "", text2: str = "", text3: str = "", font_path: str = "",
                        small_font_path: str = "", output_path: str = "",
                        color1: str = "#07098A", color2: str = "#3FAED4",
                        width: int = 1937, height: int = 1022,
                        angle=115, text_type: TextType = TextType.WHITE, bg_type: BgType = BgType.ALPHA,
                        direction=Direction.HORIZONTAL, size_ratio=1):
    """
    生成带有渐变蒙版的魔禁风格字体图片：
    :param text: 要生成的文字
    :param font_path: 字体文件路径
    :param small_font_path: 小字体文件路径
    :param output_path: 输出图片路径
    :param color1: 渐变色1，默认为蓝色
    :param color2: 渐变色2，默认为青色
    :param width: 图片宽度，默认为 1937
    :param height: 图片高度，默认为 1022
    :param angle: 渐变角度，默认为 115 度
    :return: None
    """
    # 创建一个透明背景，绘制黑色文字
    text_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_img)
    try:
        _ = ImageFont.truetype(font_path, 100)  # 测试字体加载
    except Exception as e:
        print(f"没有这个字体， {e}，do，御坂无情地报错道。")
        return

    text = f'とある{text1}の{text2}'
    len1, len2 = len(text1), len(text2)
    where_rect = 4 + len1
    # 定义每个字的相对中心坐标（相对于画布中心）和相对高度（占画布高度的比例）
    xy = [(-0.4189, -0.2725), (-0.2630, -0.2079), (-0.1631, -0.2920),
          (0.0100, -0.2607), (0.2235, -0.2162), (0.4091, -0.2118),
          (-0.3170, 0.2392), (-0.0836, 0.1898), (0.1153, 0.1815),
          (0.3273, 0.2255)]
    size = [0.4471, 0.3023, 0.2084, 0.4784, 0.3757,
            0.3297, 0.5000, 0.3992, 0.4099, 0.5430]

    def draw_text(pen, i, word, color=(0, 0, 0, 255)):
        """写一个字符"""
        char_height = int(height * size[i])
        font = ImageFont.truetype(font_path, char_height)
        # 获取字符宽度
        char_bbox = font.getbbox(word)
        char_width = char_bbox[2] - char_bbox[0]
        abs_x = int(width / 2 + xy[i][0] * width - char_width / 2)
        abs_y = int(height / 2 + xy[i][1] * height - char_height / 2)
        pen.text((abs_x, abs_y), word, font=font, fill=color)

    # 在 text_img 上绘制黑色文字
    for i, char in enumerate(text):
        if i == where_rect:
            rx, ry = 0.258 * width / 2, 0.48 * height / 2
            ax, ay = int(width / 2 + xy[i][0] * width), int(height / 2 + xy[i][1] * height)
            draw.rectangle([ax - rx, ay - ry, ax + rx, ay + ry], fill=(0, 0, 0, 255))
            draw_text(draw, i, char, color=(0, 0, 0, 0))
        else:
            draw_text(draw, i, char)

    # 保存文字区域的不透明度
    text_alpha = text_img.split()[3]  # 文字图层的 alpha 通道

    # 生成渐变蒙版
    # 创建灰度图（L 模式）作为渐变蒙版
    gradient_mask = Image.new("L", (width, height), 0)
    grad_draw = ImageDraw.Draw(gradient_mask)

    angle_rad = math.radians(angle)
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    # 先遍历整个图像计算 offset 的最小和最大值，用于归一化
    min_offset = float("inf")
    max_offset = float("-inf")
    for x in range(width):
        for y in range(height):
            offset = x * dx + y * dy
            if offset < min_offset:
                min_offset = offset
            if offset > max_offset:
                max_offset = offset
    # 根据归一化后的比例，赋值灰度（0～255）
    for x in range(width):
        for y in range(height):
            offset = x * dx + y * dy
            factor = (offset - min_offset) / (max_offset - min_offset)
            value = int(255 * factor)
            grad_draw.point((x, y), fill=value)

    # 生成渐变色图层
    color1_img = Image.new("RGBA", (width, height), color1)
    color2_img = Image.new("RGBA", (width, height), color2)
    gradient_img = Image.composite(color1_img, color2_img, gradient_mask)
    # gradient_img.show()
    # 将渐变图层的颜色应用到文字区域
    # 用文字的 alpha 作为蒙版，使渐变只在文字区域显示，并恢复原来的不透明度
    gradient_img.putalpha(text_alpha)
    last_draw = ImageDraw.Draw(gradient_img)

    if text_type == TextType.WHITE or text_type == TextType.HARD_OUTFIT or text_type == TextType.SOFT_OUTFIT:
        draw_text(last_draw, where_rect, text[where_rect], color=(255, 255, 255, 255))

    # 保存最终结果
    gradient_img.show()

    # gradient_img.save(output_path)
    print(f"Image saved to: {output_path}")


if __name__ == "__main__":
    # text = "とある魔術の禁書目録"
    try:
        a="ppp"
        print(a/10)
    except Exception as e:
        print(e)
    exit(0)
    text = "とある學都の標題工房"
    output_path = "output.png"
    generate_font_image(text1="學都", text2="標題工房", font_path=resource_path("fonts/XiaoMingChaoPro-B-6.otf"),
                        small_font_path="",
                        output_path=output_path, angle=115,
                        color1="#D52034", color2="#FEB340")

