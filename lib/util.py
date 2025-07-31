from math import sqrt

alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 .'

def is_alphanumeric(key: str) -> bool:
    return key in alphanumeric

def circle_col(center: list[float], radius: float, point: list[float]) -> bool:
    dx = pow(point[0] - center[0], 2)
    dy = pow(point[1] - center[1], 2)
    return sqrt(dx+dy) <= radius

def dist(p1: list[float], p2: list[float]):
    x = pow(p1[0] - p2[0], 2)
    y = pow(p1[1] - p2[1], 2)
    return sqrt(x + y)
