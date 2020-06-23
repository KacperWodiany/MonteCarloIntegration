import mc_integration as mc
import argparse
import numpy as np
import math  # Importing math since user can use some predefined functions as an integrand


def build_integrand(dim, func_str):
    integrand_str = list('lambda ')
    for i in range(dim):
        integrand_str.append('x' + str(i + 1))
        integrand_str.append(',')
    integrand_str[-1] = ': ' + func_str
    return ''.join(integrand_str)


def run(func, dim, low, upp, m, rep):
    integrand = eval(build_integrand(dim, func))
    method = mc.ant_uniform if m else np.random.uniform
    try:
        integral = mc.integrate(integrand, np.array(low), np.array(upp), dim, method, rep)
        print(f'Integral value: {integral}')
    except NameError as ne:
        print("Haven't you forgot to number function's arguments. Instead of x, y, ... should be x1, x2, ...")
        raise ne
    except TypeError as te:
        print("Apostrophes(') are redundant while typing function name")
        raise te


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monte Carlo Integral Calculator')
    parser.add_argument('-f', '--function', type=str, required=True,
                        help="Function to be integrated. No white space allowed! "
                             "Given by string, i.e. to integrate f(x1, x2) = x1 + x2,"
                             " the input string is x1+x2. Important, use name x1, x2, ... for variables."
                             "To use predefined mathematical function, use functions form math module,"
                             " i.e. f(x1) = exp(x1), the input string is math.exp(x1)")
    parser.add_argument('-d', type=int, default=1, help='Number of integrating variables')
    parser.add_argument('-l', '--lower-limit', required=True, type=np.float, nargs='+',
                        help='Array of lower limits. Even if dim == 1, one-element array should be passed')
    parser.add_argument('-u', '--upper-limit', required=True, type=np.float, nargs='+',
                        help='Array of upper limits. Even if dim == 1, one-element array should be passed')
    parser.add_argument('-m', '--method', type=int, default=1,
                        help='0-Crude Monte Carlo(CMC), 1-Antithetic Variates')
    parser.add_argument('-rep', type=int, default=10 ** 4, help='Number of replications')

    args = parser.parse_args()

    run(args.function, args.d, args.lower_limit,
        args.upper_limit, args.method, args.rep)
