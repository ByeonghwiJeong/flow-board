import re


def password_valid(x):
    if len(x) < 6:
        return (False, "Enter 6 or more English letters and numbers")
    elif not re.search('[0-9]+', x):
        return (False, "Enter 1 or more numbers")
    return (True, None)