from PIL import Image


# Add Margin
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


# Keyword Conversion
def keyword_conversion(para_str):
    if "AITA" in para_str:
        para_str = para_str.replace('AITA', 'Am I the asshole')
    elif "Aita" in para_str:
        para_str = para_str.replace('Aita', 'Am I the asshole')
    elif "aita" in para_str:
        para_str = para_str.replace('aita', 'Am I the asshole')
    elif "WIBTA" in para_str:
        para_str = para_str.replace('WIBTA', 'Will I be the asshole')
    elif "Wibta" in para_str:
        para_str = para_str.replace('Wibta', 'Will I be the asshole')
    elif "wibta" in para_str:
        para_str = para_str.replace('wibta', 'Will I be the asshole')

    print("Keyword Conversion complete")
    return para_str


