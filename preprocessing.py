from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

IMAGE_ROWS = 567
IMAGE_COLS = 589
IMAGE_SIZE = 589  # max(rows, cols) # 57 # 227
SLICES_DIR = 'slices_z(beispiel)/'

# load images: list
img_dir = SLICES_DIR
images = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith('tif'):
        images.append(file)
images.sort()

images_x = [Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255) for item in range(IMAGE_SIZE)]
images_y = [Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255) for item in range(IMAGE_SIZE)]
images_z = [Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255) for item in range(IMAGE_SIZE)]

images_x = [np.array(img) for img in images_x]
images_y = [np.array(img) for img in images_y]
images_z = [np.array(img) for img in images_z]

for z, img in enumerate(images):
    img = np.array(np.array(Image.open(SLICES_DIR + img)))
    for i in range(IMAGE_ROWS):  # x-axis
        for j in range(IMAGE_COLS):  # y-axis
            color = img[i][j]
            images_x[i][z][j] = color
            images_y[j][i][z] = color
            images_z[z][i][j] = color

index = 0
for img in images_x:
    im = Image.fromarray(img)
    im.save('slices_x/x'+str(index).zfill(3)+'.tif')
    index += 1

index = 0
for img in images_y:
    im = Image.fromarray(img)
    im.save('slices_y/y'+str(index).zfill(3)+'.tif')
    index += 1

index = 0
for img in images_z:
    im = Image.fromarray(img)
    im.save('slices_z/z'+str(index).zfill(3)+'.tif')
    index += 1
