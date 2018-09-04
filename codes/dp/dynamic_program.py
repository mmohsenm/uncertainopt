__author__ = "Mohsen Moarefdoost"
__license__ = ""
__version__ = "1.0"
__doc__ = "dynamic programming implementation of production planning problem"

import functools


def keep_function_history(fn):
    history = {}

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        arguments = [_ for _ in kwargs.items()]
        arguments = sorted(arguments, key=lambda _: _[0].lower())
        arguments.append(args)
        arguments = tuple(arguments)
        try:
            return history[arguments]
        except KeyError:
            retval = fn(*args, **kwargs)
            history[arguments] = retval
            return retval

    return wrapped


class DynamicProgram(object):
    pass


if __name__ == "__main__":
    pass
