__author__ = 'arubtsov'

from PIL import Image, ImageStat
import pyglet
from pyglet.gl import gl
import math
from random import randint

wDices = 40
hDices = 40
# switch to optional total number of dices and aspect ratio


def pil_to_pyg(pil_image):
    w, h = pil_image.size
    return pyglet.image.ImageData(w, h, 'rgb', pil_image.tostring(), pitch=-w * 3)


# RGB -> XYZ(2deg, d65) -> L*ab
def rgb2lab(input_color):
    num = 0
    rgb = [0, 0, 0]

    for value in input_color:
        value = float(value) / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value /= 12.92
        rgb[num] = value * 100
        num += 1

    xyz = [0, 0, 0]
    x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    xyz[0] = round(x, 4) / 95.047
    xyz[1] = round(y, 4) / 100.0
    xyz[2] = round(z, 4) / 108.883

    num = 0
    for value in xyz:
        if value > 0.008856:
            value = value ** 1/3
        else:
            value = (7.787 * value) + (16 / 116)
        xyz[num] = value
        num += 1

    lab = [0, 0, 0]
    lab[0] = round((116 * xyz[1]) - 16, 4)
    lab[1] = round(500 * (xyz[0] - xyz[1]), 4)
    lab[2] = round(200 * (xyz[1] - xyz[2]), 4)

    return lab


def colors_to_texture(colors):
    img = Image.new("RGB", (1, len(colors)))
    for i in range(len(colors)):
        img.putpixel((0, i), tuple(colors[i]))
    return img


def closest_color(color, color_array):
    orig_lab = rgb2lab(color)
    out = tuple()
    minim = 5000
    for c in color_array:
        tmp_lab = rgb2lab(c)
        delta = math.sqrt(
            (tmp_lab[0] - orig_lab[0]) ** 2 + (tmp_lab[1] - orig_lab[1]) ** 2 + (tmp_lab[2] - orig_lab[2]) ** 2)
        if delta < minim:
            minim = delta
            out = c
    return tuple(out)


def process(img_path, palete):
    pil_image = Image.open(img_path)
    out_image = Image.new("RGB", (wDices, hDices))
    im_w, im_h = pil_image.size
    w_step, h_step = int(math.ceil(im_w / wDices)), int(math.ceil(im_h / hDices))
    for i in range(0, wDices):
        for j in range(0, hDices):
            box = pil_image.crop((i * w_step, j * h_step, (i + 1) * w_step, (j + 1) * h_step))
            stat = ImageStat.Stat(box)
            # out_image.putpixel((i, j), tuple(map(lambda x: int(math.ceil(x)), stat.mean)))
            out_image.putpixel((i, j), closest_color(stat.mean, palete))
    return out_image

num_colors = 50
rand_colors = [[randint(0, 255) for _ in range(3)] for _ in range(num_colors)]

test_image = "./res/Lenna.png"
proc_img = process(test_image, rand_colors)

window = pyglet.window.Window(width=800, height=600)

main_image = pil_to_pyg(proc_img)
main_tex = main_image.get_texture()
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
main_tex.width = 500
main_tex.height = 500
colors_widget = pil_to_pyg(colors_to_texture(rand_colors))
colors_tex = colors_widget.get_texture()
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
colors_tex.width = 100
colors_tex.height = 300

@window.event
def on_draw():
    window.clear()
    main_tex.blit(0, 0)
    colors_tex.blit(600, 0)


pyglet.app.run()

