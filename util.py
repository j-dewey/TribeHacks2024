from math import sqrt


alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 .'

def is_alphanumeric(key: str) -> bool:
    return key in alphanumeric

def circle_col(center: list[float], radius: float, point: list[float]) -> bool:
    dx = pow(point[0] - center[0], 2)
    dy = pow(point[1] - center[1], 2)
    return sqrt(dx+dy) <= radius