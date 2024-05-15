import fontforge
import os

export_folder = "export"
export_src = "src"
export_dist = 'dist'
font_file_export_from = "ProductIconsFont032.ttf"

font_file_export_from_path = os.path.join(export_folder, export_src, font_file_export_from)
svg_file_export_to_path = os.path.join(export_folder, export_dist)

def scale_glyph(glyph, descent):
    # Calculate the original bounding box dimensions
    target_size = 990
    bbox = glyph.boundingBox()
    orig_width = bbox[2] - bbox[0]
    orig_height = bbox[3] - bbox[1]

    codepoint = f"{glyph.unicode:04X}"
    # print(orig_width, orig_height, glyph.width, glyph.vwidth, codepoint)

    scale_factor_width = target_size / orig_width if orig_width != 0 else 1
    scale_factor_height = target_size / orig_height if orig_height != 0 else 1

    scale_factor = min(scale_factor_width, scale_factor_height)

    scale_matrix = (scale_factor, 0, 0, scale_factor, 0, 0)

    glyph.transform(scale_matrix)

    glyph.width = target_size
    glyph.vwidth = target_size

    # transform center in position

    bboxT = glyph.boundingBox()
    transformed_width = bboxT[2] - bboxT[0]
    transformed_height = bboxT[3] - bboxT[1]

    left_offset = (target_size - transformed_width) / 2
    top_offset = (target_size - transformed_height) / 2

    translate_x = -bboxT[0] + left_offset
    translate_y = -bboxT[1] + top_offset
    print(codepoint)

    offset_left = bboxT[0]
    offset_top =  -1 * (descent + bboxT[1])
    glyph.transform((1, 0, 0, 1, -offset_left, offset_top))

    bboxA = glyph.boundingBox()

    vect_h = 1000 - abs(bboxA[3] + abs(bboxA[1]))
    vect_h_half =  vect_h / 2

    print(glyph.vwidth)
    print(bboxA[1], bboxA[3], descent, vect_h_half)
    print('----------------')

    glyph.transform((1, 0, 0, 1, 0, vect_h_half))

    glyph.width = target_size
    glyph.vwidth = target_size


def export_glyphs_as_svg(font_path, svg_path):
    # Load the font
    font = fontforge.open(font_path)
    # print(dir(font))
    print(font.os2_typodescent)
    descent = abs(font.os2_typodescent)
    # Create a directory for SVGs if it doesn't exist
    if not os.path.exists(svg_path):
        os.makedirs(svg_path)

    # Loop through all glyphs in the font
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            # Scale the glyph

            # Get the Unicode codepoint of the glyph as a hex string
            codepoint = f"{glyph.unicode:04X}"
            # Set the file name with the codepoint
            filename = os.path.join(svg_path, f"{codepoint}.svg")
            # Export the glyph as SVG
            scale_glyph(glyph, descent)

            glyph.export(filename)

    # Close the font
    font.close()

# Example usage: specify the path to your font file and desired dimensions
export_glyphs_as_svg(font_file_export_from_path, svg_file_export_to_path)
