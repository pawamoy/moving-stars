import sys


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
