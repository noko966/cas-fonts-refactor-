import fontforge
import os
import json
import uuid
import shutil

printEnabled = True


def custom_print(*args, **kwargs):
    if printEnabled:
        print(*args, **kwargs)


def load_name_mapping(filename):
    with open(filename, "r") as file:
        return json.load(file)


def update_name_mapping(new_names_mapping):
    name_mapping = load_name_mapping(name_mapping_json_path)

    name_mapping.update(new_names_mapping)

    save_name_mapping(name_mapping, name_mapping_json_path)
    print("Updated name mapping has been saved.")


def save_name_mapping(mapping, path):
    with open(path, "w") as file:
        json.dump(mapping, file, indent=4)


def scale_glyph(glyph):
    target_width = 1024
    target_height = 1024
    bbox = glyph.boundingBox()
    glyph_width = bbox[2] - bbox[0]
    glyph_height = bbox[3] - bbox[1]


    # Calculate scaling factors
    scale_x = target_width / glyph_width if glyph_width != 0 else 1
    scale_y = target_height / glyph_height if glyph_width != 0 else 1
    scale_factor = min(scale_x, scale_y) * 0.87

    # Apply scaling to fit within the target bounding box
    glyph.transform((scale_factor, 0, 0, scale_factor, 0, 0))

    # Get the new bounding box after scaling
    bbox = glyph.boundingBox()
    glyph_width = bbox[2] - bbox[0]
    glyph_height = bbox[3] - bbox[1]

    # Calculate the translation needed to center the glyph
    left_offset = (target_width - glyph_width) / 2
    top_offset = (target_height - glyph_height) / 2
    translate_x = -bbox[0] + left_offset
    translate_y = -bbox[1] + top_offset

    # Apply the translation to center the glyph
    glyph.transform((1, 0, 0, 1, translate_x, translate_y))

    # Set the glyph width and vertical width to the target size
    glyph.width = target_width
    glyph.vwidth = target_height



new_names_mapping = {}

# Config for Paths and Names
source_folder = "src"
icons_folder = "icons"
source_blank_font = "menu_icons_font.ttf"

src_icons_path = os.path.join(source_folder, icons_folder)
font = fontforge.open(os.path.join(source_folder, source_blank_font))
css_class_prefix = "dynamic_icon"
font_file_name = "menu_icons_font"
font_family_name = "iconsDinamicMenu"
css_class_additional = "cw_icon"
ico_preview_size = "24"
files = os.listdir(src_icons_path)
name_mapping_json_path = os.path.join(source_folder, "name_mapping.json")
starter_ttf_font_path = os.path.join(source_folder, source_blank_font)

name_mapping = load_name_mapping(name_mapping_json_path)

filesArray = []

html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="styles.css" />
    <style>
    *{
      box-sizing: border-box;
    }
    html, body{
      margin: 0;
      padding: 0;
    }
  .icons_container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* This ensures each item can grow but starts with a minimum width of 150px */
    justify-content: center;
    align-items: center;
    column-gap: 12px;
    row-gap: 12px;
    padding: 16px;
    background: var(--bodyBg);
}

.icon_demo {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: var(--dominantBg);
    border: 1px solid var(--dominantBg2);
    row-gap: 6px;
    border-radius: 12px;
    padding: 12px;
    transition: all 0.3s;
    cursor: pointer;
    overflow: hidden;
}

html {
  background: var(--bodyBg);
  color: var(--bodyTxt);
  font-family: Arial;
}

.btn_demo_row{
    display: flex;
    align-items: center;
    column-gap: 8px;
    justify-content: space-between;
}

.icon_demo_row{
    display: flex;
    align-items: center;
    justify-content: center;
    column-gap: 8px;
}

button.btn_demo {
    appearance: none;
    border: 0;
    text-wrap: nowrap;
    font-size: 8px;
    background: var(--dominantBg2);
    border: 1px solid var(--dominantBg3);
    color: var(--dominantTxt);
    border-radius: 7px;
    cursor: pointer;
    height: 22px;
    text-transform: capitalize;
}

button.btn_demo:active{
  background: var(--dominantBg3);
}

.message {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }

  </style>
  </head>
  <body>
    <div class="icons_container">
  
"""

# Generate CSS content
css_content = f"""
@font-face {{
  font-family: "{font_family_name}";
  src: url("{font_file_name}.eot");
  src: url("{font_file_name}.eot?#iefix") format("embedded-opentype"),
    url("{font_file_name}.woff2") format("woff2"),
    url("{font_file_name}.woff") format("woff"),
    url("{font_file_name}.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: block;
}}




:root{{
  --bodyBg: #121212;
  --bodyBg2: #334655;
  --bodyBg3: #445c6f;
  --bodyTxt: #ccc;
  --dominantBg: #0b293d;
  --dominantBg2: #14496d;
  --dominantBg3: #286a96;
  --dominantTxt: #fefefe;
  --accentBg: #00b6ff;
  --accentBg2: #33454d;
  --accentTxt: rgba(0, 0, 0, 0.97);
  --icoSize: {ico_preview_size}px;
}}

.dynamic_icon {{
  font-family: "iconsDinamicMenu";
  font-size: 46px;
  line-height: 0.8;
}}


.icon_demo:hover {{
}}

.icon_demo > strong {{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.icon_demo_e {{
    background: var(--dominantBg2);
    border: 1px solid var(--dominantBg3);
    row-gap: 12px;
    border-radius: 12px; 
}}

[class^="{css_class_additional}"],
[class*=" {css_class_additional}"],
.{css_class_additional} {{
  font-family: "{font_family_name}";
  display: inline-block;
  flex-shrink: 0;
  width: var(--icoSize);
  height: var(--icoSize);
font-size: calc(var(--icoSize) * 2);
  text-align: center;
  vertical-align: middle;
  font-weight: normal;
  font-style: normal;
  speak: none;
  text-decoration: inherit;
  text-transform: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  direction: ltr !important;
  content: "\\E0000";
}}

.ico_size-xs{{
    --icoSize: 16px;
}}
.ico_size-sm{{
    --icoSize: 20px;
}}
.ico_size-md{{
    --icoSize: 24px;
}}
.ico_size-lg{{
    --icoSize: 28px;
}}
.ico_size-xl{{
    --icoSize: 32px;
}}
"""



def transform_name(name):
    # Make the entire name lowercase
    name = name.lower()
    
    # Replace spaces with underscores
    transformed_name = name.replace(" ", "_")
    
    return transformed_name


for file in files:
    filesArray.append(file)

custom_print(filesArray)


last_index = None

# Loop through Private Use Area from U+E000 to U+E7B5

for code_point in range(0xE000, 0xE7B6):
    glyph_code = "uni" + format(
        code_point, "04X"
    )  # Converts code point to a four-character hexadecimal string
    if glyph_code in font:  # Checks if the glyph exists in the font
        # custom_print(f"exist {glyph_code}")
        name = name_mapping.get(str(code_point), "Unknown")
        html_content += f"""
        <div class="icon_demo">
        <div class="icon_demo_row">
          <i style="background: var(--dominantBg2);" class="{css_class_additional} copy_symbol_js ico_size-xs">&#x{format(code_point, 'X')};</i>
          <i style="background: var(--dominantBg2);" class="{css_class_additional}_{transform_name(name)} copy_class_js ico_size-sm"></i>
          <i style="background: var(--dominantBg2);" class="{css_class_additional}_{transform_name(name)} copy_class_js ico_size-md"></i>
          <i style="background: var(--dominantBg2);" class="{css_class_additional}_{transform_name(name)} copy_class_js ico_size-lg"></i>
          <i style="background: var(--dominantBg2);" class="{css_class_additional}_{transform_name(name)} copy_class_js ico_size-xl"></i>
        </div>
        <strong>{name}</strong>
        <span>#{code_point}</span>
        <div class="btn_demo_row">
          <button class='btn_demo copy_class_btn_js'>copy class</button>
          <button class='btn_demo copy_symbol_btn_js'>copy symbol</button>
        </div>
      </div>
      """
        
        css_content += f"""
    .{css_class_additional}_{transform_name(name)}::before {{
        content: "\\{format(code_point, '04X')}";  
    }}
    """
        
        glyph = font[glyph_code]
        
        scale_glyph(glyph)

        last_index = code_point
    else:
        # html_content += f"""
        #   <div class="icon_demo icon_demo_e">
        #     <i class="{css_class_additional}">&#x{format(code_point, 'X')};</i>
        #     <span>#{code_point}</span>
        #   </div>
        # """
        custom_print(f"does not exist {glyph_code}")


if last_index is not None:
    # Files to add as glyphs
    files = os.listdir(src_icons_path)
    start_index = last_index + 1

    for idx, file in enumerate(files, start=start_index):
        if idx >= 0xE7B6:  # Prevent overflow of PUA range
            break
        glyph_code = "uni" + format(idx, "04X")
        glyph = font.createChar(idx, glyph_code)
        glyph.importOutlines(os.path.join(src_icons_path, file))

        scale_x = 0.5  # 50% scaling on the x-axis
        scale_y = 0.5  # 50% scaling on the y-axis

        scale_matrix = (scale_x, 0, 0, scale_y, 0, 0)

        glyph.transform(scale_matrix)

        bbox = glyph.boundingBox()

        glyph_width = bbox[2] - bbox[0]  # xMax - xMin
        glyph_height = bbox[3] - bbox[1]  # yMax - yMin

        target_width = 1024
        target_height = 1024

        left_offset = (target_width - glyph_width) / 2
        top_offset = (target_height - glyph_height) / 2

        translate_x = -bbox[0] + left_offset
        translate_y = -bbox[1] + top_offset

        bbox = glyph.boundingBox()

        glyph.transform((1, 0, 0, 1, 0, translate_y))

        glyph.width = target_width
        glyph.vwidth = target_height

        name = os.path.splitext(file)[0]

        html_content += f"""
        <div class="icon_demo">
          <i class="{css_class_additional}">&#x{format(idx, 'X')};</i>
          <strong>{name}</strong>
          <span>#{idx}</span>
        </div>
      """

        new_names_mapping[idx] = name

        


else:
    custom_print("No existing glyphs were found in the specified range.")

# update_name_mapping(new_names_mapping)
print(new_names_mapping)

html_content += "\n</div>"


font.save("dist/output-font.sfd")

font.generate(f"dist/{font_file_name}.ttf")
font.generate(f"dist/{font_file_name}.eot")
font.generate(f"dist/{font_file_name}.woff")
font.generate(f"dist/{font_file_name}.woff2")


html_content += """
          <div class="message" id="copyMessage">Copied!</div>
      </body>
      <script>
        document.querySelectorAll('.copy_symbol_btn_js').forEach(item => {
            item.addEventListener('click', function() {
                const iconContent = this.parentElement.parentElement.querySelector('.copy_symbol_js').textContent;
                navigator.clipboard.writeText(iconContent).then(() => {
                    const messageDiv = document.getElementById('copyMessage');
                    messageDiv.style.display = 'block';  // Show the message
                    setTimeout(() => {
                        messageDiv.style.display = 'none';  // Hide the message after 2 seconds
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });

        document.querySelectorAll('.copy_class_btn_js').forEach(item => {
            item.addEventListener('click', function() {
                const iconContent = this.parentElement.parentElement.querySelector('.copy_class_js').classList[0];
                navigator.clipboard.writeText(iconContent).then(() => {
                    const messageDiv = document.getElementById('copyMessage');
                    messageDiv.style.display = 'block';  // Show the message
                    setTimeout(() => {
                        messageDiv.style.display = 'none';  // Hide the message after 2 seconds
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });
        </script>
</html>
    """

# Save HTML file
html_file_path = "dist/index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "dist/styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)
