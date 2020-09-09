from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d


def triangles(img) -> list:
    """
    :param img: name of a black and white image in the slices folder
    :return: facets: triangulation of img
    """
    im = Image.open('slices/'+img)
    img = np.array(im)
    facets = []
    for i in range(0, 227):
        for j in range(0, 227):
            if img[i][j] == 0:  # if pixel is black
                # traverse clock-wise; 0 = basement level
                facets.append([[i + 1, j + 1, 0], [i + 1, j, 0], [i, j, 0]])  # upper triangle of pixel
                facets.append([[i, j + 1, 0], [i + 1, j + 1, 0], [i, j, 0]])  # lower triangle
    facets = np.array(facets)
    return facets


def get_bottom(images: list) -> list:
    """
    :param images: a (ordered) list of images
    :return: facets of first image in images
    """
    return triangles(images[0])


def get_roof(images: list) -> list:
    """
    :param images: A (ordered) list of images
    :return: Triangulation of last image in images
    """
    # ToDo: add vertices of triangle clock-wise to have correct orientation of contour
    n = len(images)
    return triangles(images[n - 1])


def x_scan(img1, img2) -> list:
    return


def y_scan(img1, img2) -> list:
    return


def z_scan(img1, img2) -> list:
    return


def merge(img1, img2) -> list:
    triangulation = [x_scan(img1, img2), y_scan(img1, img2), z_scan(img1, img2)]
    return triangulation


def triangulate(images: list) -> list:
    """
    :param images: A (ordered) list of images
    :return: triangulation: Triangulation of images as list of Facet objects
    """
    n = len(images)
    triangulation = [get_bottom(images), get_roof(images)]  # unordered list of Facets
    for level in range(0, n-2):
        triangulation.append(merge(images[level], images[level + 1]))
    return triangulation


# load images: list
img_dir = "slices"
images = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images.append(file)
images.sort()

# create stl file:

facets = get_bottom(images)

# ToDo:
#  1. merge first and second level: facets = merge(images[0],images[1])
#  2. generalize for all levels, i.e. create stl from all images: triangulation = triangulate(images)

# create the mesh
level = mesh.Mesh(np.zeros(facets.shape[0], dtype=mesh.Mesh.dtype))
level.vectors = facets

# write the mesh to file "level.stl"
level.save('level.stl')

# plot:

figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# load the stl files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('level.stl')
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
