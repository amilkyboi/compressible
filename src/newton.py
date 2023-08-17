# module newton
'''
A simple Newton-Raphson solver.
'''

from typing import Callable

def newton_raphson(func: Callable, dfunc: Callable, root: float, n_max: int=100,
                   tol: float=1e-11) -> tuple[float, int]:
    '''
    Simple implementation of the Newton-Raphson method. Returns the final root guess and the number
    of iterations required.

    Args:
        func (Callable): function set equal to zero
        dfunc (Callable): analytical derivative of the function
        root (float): initial guess for the root
        n_max (int, optional): maximum number of iterations, defaults to 100
        tol (float, optional): minimum tolerance between iterations, defaults to 1e-11

    Returns:
        tuple[float, int]: final root, number of iterations
    '''

    i = 0

    for i in range(n_max):
        change = func(root) / dfunc(root)
        root  -= change

        if abs(change) < tol:
            break

    return root, i
