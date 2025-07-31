from math import sqrt

alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 .'

'''
    Is a character alphanumerical
'''
def is_alphanumeric(key: str) -> bool:
    return key in alphanumeric and len(key) == 1

'''
    Is a point contained within a circle?
'''
def circle_col(center: list[float], radius: float, point: list[float]) -> bool:
    dx = pow(point[0] - center[0], 2)
    dy = pow(point[1] - center[1], 2)
    return sqrt(dx+dy) <= radius

'''
    The distance between 2 points
'''
def dist(p1: list[float], p2: list[float]):
    x = pow(p1[0] - p2[0], 2)
    y = pow(p1[1] - p2[1], 2)
    return sqrt(x + y)
