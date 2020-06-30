from sys import argv, stderr

from PIL import Image


def loadImages(i1, i2):
    temp1 = Image.open(i1).convert("RGBA")
    temp2 = Image.open(i2).convert("RGBA").resize(temp1.size)
    return temp1, temp2


def compare(i1, i2, diff_percent=10, diff_color=(255, 0, 0)):
    cls = lambda inp: [inp.getpixel((width, height)) for height in range(inp.size[1]) for width in range(inp.size[0])]
    i1_colors, i2_colors = cls(i1), cls(i2)
    size = [(width, height) for height in range(i1.size[1]) for width in range(i1.size[0])]
    color_diff = [abs(sum(i1_colors[pixel]) - sum(i2_colors[pixel])) for pixel in range(len(i1_colors))]
    mn = min(color_diff)
    m = max(color_diff) - mn
    color_diff_bool = [(pixel - mn) / m * 100 >= diff_percent for pixel in color_diff]
    for i in range(len(color_diff_bool)):
        if color_diff_bool[i]:
            i1.putpixel(size[i], diff_color)
        else:
            temp = list(i1.getpixel(size[i]))
            temp[-1] = 127
            i1.putpixel(size[i], tuple(temp))
    return i1


if __name__ == '__main__':
    if not len(argv) >= 3:
        stderr.writelines("You must include 2 images to compare")
        exit(1)
    img1, img2 = loadImages(argv[1], argv[2])
    img = compare(img1, img2)
    img.show()
    if len(argv) >= 4: img.save(argv[3])
