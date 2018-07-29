from libcpp.string cimport string

cdef extern from "gmp_prime.h":
    cdef int rabin_miller(string num, int trials)
    
    
def is_prime(num, trials=10):
    b = bytes(ord(digit) for digit in str(num))
    return rabin_miller(b, trials)
