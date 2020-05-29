from PIL import Image

def get_image_color_count (im):
    w, h = im.size
    pix = im.load()
    color_count = {}

    for i in range(w):
        for j in range(h):
            if pix[i,j] in color_count:
                color_count[pix[i,j]] = color_count[pix[i,j]] + 1
            else:
                color_count[pix[i, j]] = 1
    return color_count
    

im = Image.open("../ironman.jpg")

color_count = get_image_color_count(im)

print (color_count)
 
