# https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html
#
#  Use k-means clustering to find the most-common colors in an image
#
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import math

def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist


def make_bar(height, width, color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv_bar[0][0]
    return bar, (red, green, blue), (hue, sat, val)


def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    return [item[0] for item in bars_with_indexes]
    
def rgb_distance (rgb_og, rgb_new):
    return math.sqrt((rgb_new[0]-rgb_og[0])**2 + (rgb_new[1]-rgb_og[1])**2 + (rgb_new[2]-rgb_og[2])**2)

img = cv2.imread('../aashna.png')
height, width, _ = np.shape(img)

# reshape the image to be a simple list of RGB pixels
image = img.reshape((height * width, 3))

# we'll pick the 5 most common colors
num_clusters = 10
clusters = KMeans(n_clusters=num_clusters)
clusters.fit(image)

# count the dominant colors and put them in "buckets"
histogram = make_histogram(clusters)
# then sort them, most-common first
combined = zip(histogram, clusters.cluster_centers_)
combined = sorted(combined, key=lambda x: x[0], reverse=True)

# finally, we'll output a graphic showing the colors in order
bars = []
hsv_values = []
rgb_values = []
for index, rows in enumerate(combined):
    bar, rgb, hsv = make_bar(100, 100, rows[1])
    print(f'Bar {index + 1}')
    print(f'  RGB values: {rgb}')
    print(f'  HSV values: {hsv}')
    hsv_values.append(hsv)
    rgb_values.append(rgb)
    bars.append(bar)

# sort the bars[] list so that we can show the colored boxes sorted
# by their HSV values -- sort by hue, then saturation
sorted_bar_indexes = sort_hsvs(hsv_values)
sorted_bars = [bars[idx] for idx in sorted_bar_indexes]

#cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
#cv2.imshow(f'{num_clusters} Most Common Colors', np.hstack(bars))
#cv2.waitKey(10000)
im = Image.open("../aashna.png")

w, h = im.size

painting = Image.new(mode = "RGB", size = im.size)
for i in range(w):
    for j in range(h):
        index = 0
        min = rgb_distance(rgb_values[0], im.getpixel((i, j)))
        for rgb_index in range(len(rgb_values)):
            if (rgb_distance(rgb_values[rgb_index], im.getpixel((i, j))) < min):
                min = rgb_distance(rgb_values[rgb_index], im.getpixel((i, j)))
                index = rgb_index
        painting.putpixel((i, j), rgb_values[index])

painting.save("../aashna-painting.png")
