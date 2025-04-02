from fontTools.ttLib import TTFont


def adjust_font_half_height(font_path, output_font_path):
    """
    将字体的绘制点向上调整一半
    :param font_path: 输入字体文件路径
    :param output_font_path: 输出字体文件路径
    """
    # 加载字体
    font = TTFont(font_path)

    # 修改hhea表
    if 'hhea' in font:
        font['hhea'].ascent *= 2
        font['hhea'].descent *= 2

    # 修改OS/2表
    if 'OS/2' in font:
        font['OS/2'].sTypoAscender *= 2
        font['OS/2'].sTypoDescender *= 2

    # 保存修改后的字体
    font.save(output_font_path)
    print(f"字体已保存到: {output_font_path}")


if __name__ == "__main__":
    pass
