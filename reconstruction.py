from PIL import Image
import numpy
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Facet:
    def __init__(self, normal: Vertex, p1: Vertex, p2: Vertex, p3: Vertex):
        self.normal = normal
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


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
im = Image.open('slices/sphere_02.tif')
plt.imshow(im, cmap='gray')
plt.show()
# img = numpy.array(im)
# size = img.shape[0]  # 227

# load images: list
# triangulation = triangulate(images)
# create STL file from triangulation
