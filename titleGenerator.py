"""
File: titleGenerator.py
Description: 生成带有渐变蒙版的魔禁风格字体图片
Author: Misaka-xxw
Created: 2025-03-30
"""
import math
from enum import Enum

import numpy as np
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


magic_color = [('#07098A', 0), ('#3FAED4', 1)]
science_color = [('#D52034', 0), ('#FEB340', 1)]


def generate_font_image(text1: str = "", text2: str = "", text3: str = "", font_path: str = "",
                        small_font_path: str = "",
                        colors=None,
                        width: int = 1937, height: int = 1022,
                        angle=155, text_type: TextType = TextType.WHITE, bg_type: BgType = BgType.ALPHA,
                        direction=Direction.HORIZONTAL, size_ratio=1) -> Image.Image:
    """
    生成带有渐变蒙版的魔禁风格字体图片：
    :param text1: 文本中间部分1，例如“學都”
    :param text2: 文本中间部分2，例如“標題工房”
    :param text3: 文本底下的小字
    :param font_path: 字体文件路径
    :param small_font_path: 小字体文件路径
    :param colors: 渐变色列表，包含至少一个颜色和它们的比例，例如 [('#000000',0), ('#ffffff',100)]
    :param width: 图片宽度，默认为 1937
    :param height: 图片高度，默认为 1022
    :param angle: 渐变角度，默认为 155 度
    :return: 生成的图片对象
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
    # 使用 numpy 优化：创建灰度图（L 模式）作为渐变蒙版
    indices = np.indices((height, width))
    Y = indices[0].astype(np.float32)  # shape (height, width)
    X = indices[1].astype(np.float32)
    # 计算每个像素对应的 offset = x * dx + y * dy
    angle_rad = math.radians(angle)
    dx = math.sin(angle_rad)
    dy = math.cos(angle_rad)
    offset_arr = X * dx + Y * dy
    min_offset = offset_arr.min()
    max_offset = offset_arr.max()
    # 归一化 factor 数组，范围 [0, 1]
    factor_arr = (offset_arr - min_offset) / (max_offset - min_offset)
    # 如果未指定 colors，则使用原有两色渐变
    if colors is None:
        colors = magic_color
    stops = sorted(colors, key=lambda s: s[1])
    # 构造 stops 数组
    stops_arr = np.array([s[1] for s in stops])

    # 对每个停靠点的颜色，取出 r, g, b 分量
    def get_rgb_arr(color_str):
        from PIL import ImageColor
        r, g, b = ImageColor.getrgb(color_str)
        return r, g, b

    r_stops = np.array([get_rgb_arr(s[0])[0] for s in stops])
    g_stops = np.array([get_rgb_arr(s[0])[1] for s in stops])
    b_stops = np.array([get_rgb_arr(s[0])[2] for s in stops])
    # 对每个像素的 factor 进行线性插值，得到 r, g, b 数组
    r_interp = np.interp(factor_arr, stops_arr, r_stops).astype(np.uint8)
    g_interp = np.interp(factor_arr, stops_arr, g_stops).astype(np.uint8)
    b_interp = np.interp(factor_arr, stops_arr, b_stops).astype(np.uint8)
    # 合成渐变图层数组（RGBA），alpha 固定为 255
    gradient_arr = np.stack([r_interp, g_interp, b_interp, 255 * np.ones_like(r_interp, dtype=np.uint8)], axis=-1)
    # 转换为 PIL 图片
    gradient_img = Image.fromarray(gradient_arr, mode="RGBA")

    # 将渐变图层的颜色应用到文字区域
    # 用文字的 alpha 作为蒙版，使渐变只在文字区域显示，并恢复原来的不透明度
    gradient_img.putalpha(text_alpha)
    last_draw = ImageDraw.Draw(gradient_img)

    if text_type == TextType.WHITE or text_type == TextType.HARD_OUTFIT or text_type == TextType.SOFT_OUTFIT:
        draw_text(last_draw, where_rect, text[where_rect], color=(255, 255, 255, 255))

    # 返回最终生成的图片对象
    return gradient_img


# 辅助函数，用于将颜色字符串转换为 RGB 元组
def ImageColor_getrgb(color_str):
    from PIL import ImageColor
    return ImageColor.getrgb(color_str)


if __name__ == "__main__":
    # text = "とある魔術の禁書目録"
    text = "とある學都の標題工房"
    output_path = "output.png"
    # 示例：自定义渐变：使用 science_color
    img = generate_font_image(text1="學都", text2="標題工房",
                              font_path=resource_path("fonts/adjusted_ZauriSansItalic-Bold.ttf"),
                              small_font_path="",
                              colors=science_color)
    img.save(output_path)
    print(f"Image saved to: {output_path}")
