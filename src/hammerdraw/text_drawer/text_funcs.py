def capitalize_first(s: str) -> str:
    if (len(s) > 0):
        return s[0].upper() + s[1:]
    return s
