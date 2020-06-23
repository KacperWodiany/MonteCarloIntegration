import numpy as np
from inspect import signature
import math


# Antithetic variates
def ant_uniform(a, b, size):
    size = np.array([size]) if type(size) == int else np.array(size)
    if size[0] % 2 == 0:
        size[0] /= 2
    else:
        raise Exception(f'First element of size array must be even (is {size})')
    # Using uniform instead of rand because it approves size as array
    u = np.random.uniform(0, 1, size.astype(int))
    ant_u = 1 - u
    return rescale(np.concatenate((u, ant_u)), a, b)


def rescale(x, a, b):
    return (b - a) * x + a


def integrate(f, a, b, dim=1, rng=ant_uniform, rep=10 ** 4):
    assert len(signature(f).parameters) == dim, \
        f"Number of function's arguments ({len(signature(f).parameters)}) does not match number of dimensions ({dim})"
    assert valid_limits(a, b, dim), \
        f'Number of dimensions does not coincide with length of a and b'
    f_sample = np.apply_along_axis(Wrapper(f).wrap,
                                   axis=1,
                                   arr=rng(a, b, np.array([rep, dim])))
    return np.mean(f_sample) * np.prod(b - a)


def valid_limits(a, b, dim):
    try:
        return len(a) == len(b) == dim
    except TypeError:
        return type(a) == type(b) == int


class Wrapper:
    def __init__(self, func):
        self._func = func

    def wrap(self, args_array):
        return self._func(*args_array)


def estimator_var(f, a, b, dim=1, rng=ant_uniform, rep=10 ** 4, size=10 ** 4):
    sample = np.fromiter(map(lambda x: integrate(f, a, b, dim, rng, rep), range(size)),
                         dtype=np.float)
    return np.var(sample)
