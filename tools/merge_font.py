from fontTools.ttLib import TTFont
import copy

BASE_FONT = r"D:\Github\Toaru-Majutsu-no-Index-Title\fonts\1.ttf"
ADDON_FONT = r"D:\Github\Toaru-Majutsu-no-Index-Title\fonts\2.ttf"
OUTPUT_FONT = r"D:\Github\Toaru-Majutsu-no-Index-Title\fonts\merged.ttf"


def merge_fonts(base_path, addon_path, output_path):

    base = TTFont(base_path)
    addon = TTFont(addon_path)

    base_cmap = base.getBestCmap()
    addon_cmap = addon.getBestCmap()

    base_glyf = base["glyf"]
    addon_glyf = addon["glyf"]

    base_hmtx = base["hmtx"]
    addon_hmtx = addon["hmtx"]

    glyph_order = list(base.getGlyphOrder())

    added = 0

    for uni, name in addon_cmap.items():

        if uni in base_cmap:
            continue

        if name not in addon_glyf:
            continue

        # 避免重复 glyph
        if name in base_glyf.glyphs:
            continue

        # deep copy glyph
        base_glyf.glyphs[name] = copy.deepcopy(addon_glyf[name])

        # copy metrics
        base_hmtx.metrics[name] = addon_hmtx.metrics[name]

        glyph_order.append(name)
        base_cmap[uni] = name

        added += 1

    # 更新 glyph order
    base.setGlyphOrder(glyph_order)
    base_glyf.glyphOrder = glyph_order

    # 更新 maxp
    base["maxp"].numGlyphs = len(glyph_order)

    print("Added glyphs:", added)

    base.save(output_path)
    print("Saved:", output_path)


if __name__ == "__main__":
    merge_fonts(BASE_FONT, ADDON_FONT, OUTPUT_FONT)
