from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import math

IMAGE_SIZE = 57  # 227
SLICES_DIR_Z = 'slices_z/'
SLICES_DIR_X = 'slices_x/'
SLICES_DIR_Y = 'slices_y/'
# PLOT_DIR = 'plot/'


def triangles(img, level: int, orientation: str, dir: str) -> list:
    """
    :param img: name of a black and white image in the slices folder
    :param level: level of the sliced image
    :param orientation: one of six directions
    :return: facets: triangulation of img
    """
    if type(img) == str:
        im = Image.open('slices_' + dir + '/' + img)
        img = np.array(im)

    facets = []
    for i in range(0, IMAGE_SIZE):
        for j in range(0, IMAGE_SIZE):
            if img[i][j] == 0:  # if pixel is black
                if orientation == 'z-':  # from below
                    # traverse clock-wise
                    facets.append([[i + 1, j + 1, level], [i + 1, j, level], [i, j, level]])  # upper triangle of pixel
                    facets.append([[i, j + 1, level], [i + 1, j + 1, level], [i, j, level]])  # lower triangle
                elif orientation == 'z+':  # from above
                    facets.append([[i, j, level], [i + 1, j, level], [i + 1, j + 1, level]])
                    facets.append([[i, j, level], [i + 1, j + 1, level], [i, j + 1, level]])
                else:
                    break
    return facets


def get_bottom(images: list, dir: str) -> list:
    """
    :param dir: direction
    :param images: a (ordered) list of images
    :return: facets of first image in images
    """
    return triangles(images[0], 0, 'z-', dir)


def get_roof(images: list, dir: str) -> list:
    """
    :param dir: direction
    :param images: A (ordered) list of images
    :return: triangulation of last image in images
    """
    return triangles(images[len(images) - 1], len(images), 'z+', dir)


def merge(img1: str, img2: str, level: int, dir: str) -> list:
    """
    :param img1: title of lower image
    :param img2: title of upper image
    :param level: level of layer
    :param dir: direction of layer
    :return facets: facets resulting from two slice layers
    """

    # create images for upper and lower contour in intermediate layer
    roof = Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255)
    roof = np.array(roof)
    bottom = Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255)
    bottom = np.array(bottom)

    # load slices
    L = np.array(Image.open('slices_' + dir + '/' + img1))
    U = np.array(Image.open('slices_' + dir + '/' + img2))

    for i in range(0, IMAGE_SIZE - 1):
        for j in range(0, IMAGE_SIZE - 1):
            if L[i][j] == 0 and U[i][j] == 255:
                roof[i][j] = 0
            if U[i][j] == 0 and L[i][j] == 255:
                bottom[i][j] = 0

    return triangles(roof, level, 'z+', dir) + triangles(bottom, level, 'z-', dir)


def triangulate_z(images: list, dir: str) -> list:
    """
    :param dir: direction
    :param images: a (ordered) list of images
    :param orientation: orientation of the scan
    :return: facets: facets of all slices
    """

    facets = []
    for level in range(0, len(images) - 1):  # len(images) - 1
        level_facets = merge(images[level], images[level + 1], level + 1, dir)
        facets += level_facets
    roof_facets = get_roof(images, dir)
    bottom_facets = get_bottom(images, dir)
    facets = facets + roof_facets + bottom_facets
    facets = np.array(facets)

    return facets


# load images: list
img_dir = SLICES_DIR_Z
images_z = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images_z.append(file)
images_z = sorted(images_z)

img_dir = SLICES_DIR_X
images_x = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images_x.append(file)
images_x = sorted(images_x)

img_dir = SLICES_DIR_Y
images_y = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images_y.append(file)
images_y = sorted(images_y)

# ToDo: same for images_x and images_y

# create stl file:

facets_z = triangulate_z(images_z, 'z')
facets_x = triangulate_z(images_x, 'x')
facets_y = triangulate_z(images_y, 'y')

# to test merge:
# facets = merge(images[0], images[1], 1)

# create the mesh
level_1 = mesh.Mesh(np.zeros(facets_z.shape[0], dtype=mesh.Mesh.dtype))
level_1.vectors = facets_z
level_2 = mesh.Mesh(np.zeros(facets_x.shape[0], dtype=mesh.Mesh.dtype))
level_2.vectors = facets_x
level_2.rotate(axis=[0, 0.5, 0], theta=math.radians(270))
level_2.vectors[:, :, 2] = - level_2.vectors[:, :, 2]
level_2.vectors[:, [0, 1, 2], :] = level_2.vectors[:, [2, 1, 0], :]
level_3 = mesh.Mesh(np.zeros(facets_y.shape[0], dtype=mesh.Mesh.dtype))
level_3.vectors = facets_y
level_3.rotate(axis=[0.5, 0, 0], theta=math.radians(270))
level_3.vectors[:, :, 1] = - level_3.vectors[:, :, 1]
level_3.vectors[:, [0, 1, 2], :] = level_3.vectors[:, [2, 1, 0], :]

# scale layer height
# level.vectors[:, :, 2] *= 4  # ToDo: check, if 4 is correct!

# write the mesh to file "object.stl"
level = mesh.Mesh(np.zeros(facets_z.shape[0] + facets_x.shape[0] + facets_y.shape[0], dtype=mesh.Mesh.dtype))
one_and_two_vectors = np.append(level_1.vectors, level_2.vectors, axis=0)
level.vectors = np.append(one_and_two_vectors, level_3.vectors, axis=0)
level.save('object.stl')

# plot:

figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# load the stl files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('object.stl')
edge_color = (0 / 255, 0 / 255, 255 / 255)  # blue
collection = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
collection.set_edgecolor(edge_color)
axes.add_collection3d(collection)

# auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# plot to screen
plt.show()

# for i in range(0, 360, 30):
# axes.view_init(elev=30, azim=i)
# figure.savefig(PLOT_DIR + 'plot%d.png' % i)
