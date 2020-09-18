from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

IMAGE_SIZE = 57  # 227
SLICES_DIR = 'slices_z/'  # 'slices_0'

# load images: list
img_dir = SLICES_DIR
images_z = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith('tif'):
        images_z.append(file)
images_z.sort()

images_x = [Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255) for item in range(IMAGE_SIZE)]
images_y = [Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255) for item in range(IMAGE_SIZE)]
images_x = [np.array(img) for img in images_x]
images_y = [np.array(img) for img in images_y]

for z, img in enumerate(images_z):
    img = np.array(np.array(Image.open(SLICES_DIR + img)))
    for i in range(IMAGE_SIZE):  # x-axis
        for j in range(IMAGE_SIZE):  # y-axis
            color = img[i][j]
            images_x[i][z][j] = color
            images_y[j][i][z] = color

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
