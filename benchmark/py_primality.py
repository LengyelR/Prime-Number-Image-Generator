import random

big_nums = [2**44497 - 1, 2 ** 11213 + 1, 2 ** 23209 - 1, 2 ** 11213 - 1, 6, 3]


def rabin_miller(n):
    trials = 3
    assert n >= 2

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert (2 ** s * d == n - 1)

    # tests the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for idx in range(s):
            if pow(a, 2 ** idx * d, n) == n - 1:
                return False
        return True  # n is definitely composite

    for _ in range(trials):
        num = random.randrange(2, n)
        if try_composite(num):
            return False

    return True  # no base tested showed n as composite


if __name__ == "__main__":
    import time
    from tests.solution import PRIME_IMAGE

    start = time.clock()
    print(rabin_miller(PRIME_IMAGE))
    print(time.clock()-start, 's')
