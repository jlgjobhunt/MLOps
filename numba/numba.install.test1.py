# .MLOps/numba/numba.install.test1.py

from numba import jit

@jit(nopython=True)
def f(x):
    return x * 2

if __name__ == "__main__":
    result = f(5)
    print(result)

