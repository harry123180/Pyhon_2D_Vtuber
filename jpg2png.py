from PIL import Image
OR = "s.jpg"

from PIL import Image


def addTransparency(img, factor=0.7):
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img = Image.blend(img_blender, img, factor)
    return img

open_mouth_path = "fig_2//open_mouth.png"
close_mouth_path="fig_2//close_mouth.png"
open_eyes_path="fig_2//open_eyes.png"
close_eyes_path="fig_2//close_eyes.png"
img = Image.open(a)
img = addTransparency(img, factor=1)
img.save(a)