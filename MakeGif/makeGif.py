#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PIL import Image
import images2gif
import sys


def crop_image(path, rows, cols):
    img = Image.open(path)
    width, height = img.size
    w = width / cols
    h = height / rows
    ret = []
    for row in range(rows):
        for col in range(cols):
            # print row, col
            start_x = col * w
            start_y = row * h
            region = (start_x, start_y, start_x + w, start_y + h)
            crop_img = img.crop(region)
            ret.append(crop_img)
    return ret

def main(src, rows, cols, dest):
    # print src, rows, cols, dest
    images = crop_image(src, rows, cols)
    images2gif.writeGif(dest, images, 0.2, True, False, 0, True, 2)
    # for i in range(len(images)):
    #     images[i].save(str(i) + '.png', 'png')

if __name__ == '__main__':
    # print sys.argv
    if len(sys.argv) == 5:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])

