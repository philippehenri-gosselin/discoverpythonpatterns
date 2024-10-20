import math


def vectorAdd(a, b, w=None):
    if w is None:
        return a[0] + b[0], a[1] + b[1]
    return a[0] + w * b[0], a[1] + w * b[1]


def vectorSub(a, b):
    return a[0] - b[0], a[1] - b[1]


def vectorNorm(a):
    return math.sqrt(a[0]**2 + a[1]**2)


def vectorNormalize(a):
    norm = vectorNorm(a)
    if norm < 1e-4:
        return 0, 0
    return a[0] / norm, a[1] / norm


def vectorDist(a, b):
    diff = vectorSub(a, b)
    return vectorNorm(diff)
