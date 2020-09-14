from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d

IMAGE_SIZE = 227


def triangles(img, level: int, orientation: str) -> list:
    """
    :param img: name of a black and white image in the slices folder
    :param level: level of the sliced image
    :param orientation: one of six directions
    :return: facets: triangulation of img
    """
    if type(img) == str:
        im = Image.open('slices/'+img)
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
                elif orientation == 'x-':  # from here
                    break
                elif orientation == 'x+':  # from there
                    break
                elif orientation == 'y-':  # from left
                    break
                elif orientation == 'y+':  # from right
                    break
                else:
                    break
    return facets


def get_bottom(images: list) -> list:
    """
    :param images: a (ordered) list of images
    :return: facets of first image in images
    """
    return triangles(images[0], 0, 'z-')


def get_roof(images: list) -> list:
    """
    :param images: A (ordered) list of images
    :return: triangulation of last image in images
    """
    return triangles(images[len(images) - 1], len(images), 'z+')


def horizontal_facets(layer: np.array, i: int, j: int, level: int, orientation: str, bottom=False, roof=False) -> list:
    """
    :param roof: true, if layer is roof
    :param bottom: true, if layer is bottom
    :param orientation: orientation of layer
    :param level: level of layer
    :param j: y-coordinate of pixel
    :param i: x-coordinate of pixel
    :param layer: image as np.array from whom we retain the horizontal facets
    :return facets: horizontal facets
    """

    # determine for each edge
    facets = []

    # x direction
    if layer[i + 1][j] != 0:
        if orientation == 'z-':
            facets.append([[i+1, j + 1, level + 1], [i+1, j, level + 1], [i+1, j, level]])
            facets.append([[i+1, j + 1, level], [i+1, j+1, level + 1], [i+1, j, level]])
        if orientation == 'z+':
            facets.append([[i+1, j + 1, level - 1], [i+1, j, level - 1], [i+1, j, level]])
            facets.append([[i+1, j + 1, level], [i+1, j + 1, level - 1], [i+1, j, level]])
    if layer[i - 1][j] != 0:
        if orientation == 'z-':
            facets.append([[i, j, level], [i, j, level + 1], [i, j + 1, level + 1]])
            facets.append([[i, j, level], [i, j + 1, level + 1], [i, j + 1, level]])
        if orientation == 'z+':
            facets.append([[i, j, level], [i, j, level - 1], [i, j + 1, level - 1]])
            facets.append([[i, j, level], [i, j + 1, level - 1], [i, j + 1, level]])

    # y direction
    if layer[i][j + 1] != 0:
        if orientation == 'z-':
            facets.append([[i, j+1, level], [i, j+1, level + 1], [i+1, j+1, level + 1]])
            facets.append([[i, j+1, level], [i+1, j+1, level + 1], [i+1, j+1, level]])
        if orientation == 'z+':
            facets.append([[i, j+1, level], [i, j+1, level - 1], [i+1, j+1, level - 1]])
            facets.append([[i, j+1, level], [i+1, j+1, level - 1], [i+1, j+1, level]])

    if layer[i][j - 1] != 0:
        if orientation == 'z-':
            facets.append([[i+1, j, level + 1], [i, j, level + 1], [i, j, level]])
            facets.append([[i+1, j, level], [i+1, j, level + 1], [i, j, level]])
        if orientation == 'z+':
            facets.append([[i+1, j, level - 1], [i, j, level - 1], [i, j, level]])
            facets.append([[i+1, j, level], [i+1, j, level - 1], [i, j, level]])

    return facets


def merge(img1: str, img2: str, level: int) -> list:
    """
    :param img1: title of lower image
    :param img2: title of upper image
    :param level: level of layer
    :return facets: facets resulting from two slice layers
    """

    # create images for upper and lower contour in intermediate layer
    roof = Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255)
    roof = np.array(roof)
    bottom = Image.new('P', (IMAGE_SIZE, IMAGE_SIZE), 255)
    bottom = np.array(bottom)

    # load slices
    L = np.array(Image.open('slices/' + img1))
    U = np.array(Image.open('slices/' + img2))

    for i in range(0, IMAGE_SIZE-1):
        for j in range(0, IMAGE_SIZE-1):
            if L[i][j] == 0 and U[i][j] == 255:
                roof[i][j] = 0
            if U[i][j] == 0 and L[i][j] == 255:
                bottom[i][j] = 0

    # add horizontal facets
    facets = []
    for i in range(0, IMAGE_SIZE-1):
        for j in range(0, IMAGE_SIZE-1):
            if roof[i][j] == 0:
                facets += horizontal_facets(roof, i, j, level, 'z+')
            if bottom[i][j] == 0:
                facets += horizontal_facets(bottom, i, j, level, 'z-')

    return facets + triangles(roof, level, 'z+') + triangles(bottom, level, 'z-')


def triangulate(images: list) -> list:
    """
    :param images: a (ordered) list of images
    :return: facets: facets of all slices
    """

    facets = []
    for level in range(0, 2):  # len(images) - 1
        level_facets = merge(images[level], images[level + 1], level + 1)
        facets += level_facets

    bottom = np.array(Image.open('slices/' + images[0]))
    roof = np.array(Image.open('slices/' + images[len(images)-1]))

    # ToDo: add special horizontal facets for bottom and roof

    roof_facets = get_roof(images)
    bottom_facets = get_bottom(images)

    facets = facets + bottom_facets + roof_facets
    facets = np.array(facets)
    return facets


# load images: list
img_dir = "slices"
images = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images.append(file)
images.sort()

# create stl file:

facets = triangulate(images)

# to test merge:
# facets = merge(images[0], images[1], 1)

# create the mesh
level = mesh.Mesh(np.zeros(facets.shape[0], dtype=mesh.Mesh.dtype))
level.vectors = facets

# scale layer height
level.vectors[:, :, 2] *= 4  # ToDo: check, if 4 is correct!

# write the mesh to file "sphere.stl"
level.save('sphere.stl')

# plot:

figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# load the stl files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('sphere.stl')
edge_color = (0 / 255, 0 / 255, 255 / 255)  # blue
collection = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
collection.set_edgecolor(edge_color)
axes.add_collection3d(collection)

# auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# plot to screen
plt.show()

for i in range(0, 360, 30):
    axes.view_init(elev=30, azim=i)
    figure.savefig("plot/plot%d.png" % i)
