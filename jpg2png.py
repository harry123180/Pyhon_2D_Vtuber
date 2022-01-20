from PIL import Image
OR = "s.jpg"

from PIL import Image


def addTransparency(img, factor=0.7):
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img = Image.blend(img_blender, img, factor)
    return img

a = "close_mouth.png"
img = Image.open(a)
img = addTransparency(img, factor=1)
img.save(a)