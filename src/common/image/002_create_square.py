import json
import yaml
import os
import glob
import shutil

from PIL import Image, ImageDraw, ImageFilter

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


thumb_width = 200

path  = "data/files"

files = glob.glob(path + "/medium/*.jpg")

margin = 25

for file in files:
    opath = file.replace("/medium/", "/test2/")

    if not os.path.exists(opath):
        im = Image.open(file)
        im_thumb = crop_max_square(im).resize((thumb_width, thumb_width), Image.LANCZOS)
        im_thumb = im_thumb.crop((margin, margin, thumb_width - margin, thumb_width - margin))
        im_thumb.save(opath, quality=100)