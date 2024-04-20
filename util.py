alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 '

def is_alphanumeric(key: str) -> bool:
    return key in alphanumeric