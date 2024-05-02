import fontforge
import os

export_folder = "export"
export_src = "src"
export_dist = 'dist'
font_file_export_from = "ProductIconsFont032.ttf"

font_file_export_from_path = os.path.join(export_folder, export_src, font_file_export_from)
svg_file_export_to_path = os.path.join(export_folder, export_dist)

def scale_glyph(glyph):
    # Calculate the original bounding box dimensions
    target_size = 1024
    bbox = glyph.boundingBox()
    orig_width = bbox[2] - bbox[0]
    orig_height = bbox[3] - bbox[1]

    scale_factor_width = target_size / orig_width if orig_width != 0 else 1
    scale_factor_height = target_size / orig_height if orig_height != 0 else 1

    scale_factor = min(scale_factor_width, scale_factor_height)

    scale_matrix = (scale_factor, 0, 0, scale_factor, 0, 0)

    glyph.transform(scale_matrix)

    left_offset = (target_size - orig_width) / 2
    top_offset = (target_size - orig_height) / 2

    translate_x = -bbox[0] + left_offset
    translate_y = -bbox[1] + top_offset

    bbox = glyph.boundingBox()

    glyph.transform((1, 0, 0, 1, 0, translate_y))

    glyph.width = target_size
    glyph.vwidth = target_size


def export_glyphs_as_svg(font_path, svg_path):
    # Load the font
    font = fontforge.open(font_path)
    
    # Create a directory for SVGs if it doesn't exist
    if not os.path.exists(svg_path):
        os.makedirs(svg_path)

    # Loop through all glyphs in the font
    for glyph in font.glyphs():
        if glyph.isWorthOutputting():
            # Scale the glyph
            scale_glyph(glyph)

            # Get the Unicode codepoint of the glyph as a hex string
            codepoint = f"{glyph.unicode:04X}"
            # Set the file name with the codepoint
            filename = os.path.join(svg_path, f"{codepoint}.svg")
            # Export the glyph as SVG
            glyph.export(filename)

    # Close the font
    font.close()

# Example usage: specify the path to your font file and desired dimensions
export_glyphs_as_svg(font_file_export_from_path, svg_file_export_to_path)
