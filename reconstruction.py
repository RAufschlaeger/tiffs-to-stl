from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d


def triangles(img) -> list:
    """
    :param img: A black and white image
    :return: list_of_triangles: Triangulation of img
    """
    list_of_triangles = []
    # for every black pixel add two Facet objects to list_of_triangles:
    return list_of_triangles


def get_bottom(images: list) -> list:
    """
    :param images: A (ordered) list of images
    :return: Triangulation of first image in images
    """
    return triangles(images[0])


def get_roof(images: list) -> list:
    """
    :param images: A (ordered) list of images
    :return: Triangulation of last image in images
    """
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


# TEST:
# im = Image.open('slices/sphere_02.tif')
# plt.imshow(im, cmap='gray')
# plt.show()
# img = numpy.array(im)
# size = img.shape[0]  # 227

# load images: list
img_dir = "slices"
images = []  # list of strings
for file in os.listdir(img_dir):
    if file.endswith("tif"):
        images.append(file)

images.sort()
# print(images)

# triangulation = triangulate(images)
# should result in this format:

# define the 8 vertices of the cube
vertices = np.array([\
    [-1, -1, -1],
    [+1, -1, -1],
    [+1, +1, -1],
    [-1, +1, -1],
    [-1, -1, +1],
    [+1, -1, +1],
    [+1, +1, +1],
    [-1, +1, +1]])


# define the 12 triangles composing the cube
faces = np.array([\
    [0,3,1],
    [1,3,2],
    [0,4,7],
    [0,7,3],
    [4,5,6],
    [4,6,7],
    [5,1,2],
    [5,2,6],
    [2,3,6],
    [3,7,6],
    [0,1,5],
    [0,5,4]])

# create STL file from triangulation:

# create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# write the mesh to file "cube.stl"
cube.save('cube.stl')

# Plot:

# create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('cube.stl')
edge_color = (50 / 255, 50 / 255, 50 / 255)
collection = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
collection.set_edgecolor(edge_color)
axes.add_collection3d(collection)

# auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# if we want to change the angle ...
# axes.view_init(40, 270)

# plot to screen
plt.show()

for i in range(0, 360, 30):
    axes.view_init(elev=30, azim=i)
    figure.savefig("plot/plot%d.png" % i)
