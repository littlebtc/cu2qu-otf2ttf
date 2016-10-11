# From https://github.com/googlei18n/cu2qu/issues/47
# By anthrotype, copyright unknown

from __future__ import print_function, division, absolute_import
import sys
from fontTools.ttLib import TTFont, newTable
from cu2qu.pens import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen


# default approximation error
MAX_ERR = 1.0


def glyphs_to_quadratic(glyphs, max_err, **kwargs):
    quadGlyphs = {}
    for gname in glyphs.keys():
        glyph = glyphs[gname]
        ttPen = TTGlyphPen(glyphs)
        cu2quPen = Cu2QuPen(ttPen, max_err, **kwargs)
        glyph.draw(cu2quPen)
        quadGlyphs[gname] = ttPen.glyph()
    return quadGlyphs


def font_to_ttf(ttFont, max_err, **kwargs):
    glyphOrder = ttFont.getGlyphOrder()

    ttFont["loca"] = newTable("loca")
    ttFont["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = glyphOrder
    glyf.glyphs = glyphs_to_quadratic(ttFont.getGlyphSet(), max_err, **kwargs)
    del ttFont["CFF "]

    ttFont["maxp"] = maxp = newTable("maxp")
    maxp.tableVersion = 0b10000
    maxp.maxZones = 1
    maxp.maxTwilightPoints = 0
    maxp.maxStorage = 0
    maxp.maxFunctionDefs = 0
    maxp.maxInstructionDefs = 0
    maxp.maxStackElements = 0
    maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = max(
        len(g.components if hasattr(g, 'components') else [])
        for g in glyf.glyphs.values())

    post = ttFont["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = glyphOrder

    ttFont.sfntVersion = "\000\001\000\000"


if __name__ == "__main__":
    font = TTFont(sys.argv[1])
    font_to_ttf(font, max_err=MAX_ERR)
    font.save(sys.argv[2])
