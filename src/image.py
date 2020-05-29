from PIL import Image

def get_image_color_count (im):
    w, h = im.size
    color_count = {}

    for i in range(w):
        for j in range(h):
            if pix[i,j] in color_count:
                color_count[im.getpixel((i, j))] = color_count[im.getpixel((i, j))] + 1
            else:
                color_count[im.getpixel((i, j))] = 1
    return color_count

im = Image.open("../ironman.png")

color_count = im.histogram()

print(len(color_count))
#for x in color_count:
#    print(x)
 
 
painting = Image.new(mode = "RGB", size = im.size)
w, h = im.size
for i in range(w):
    for j in range(h):
        painting.putpixel((i, j), im.getpixel((i, j)))

print(painting.getcolors())
painting.save("../ironman-painting.png")
