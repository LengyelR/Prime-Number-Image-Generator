#include <iostream>
#include <chrono>
#include "gmp_prime.h"
#include "mpirxx.h"
#include "mpir.h"


int rabin_miller(std::string num, int trials)
{   
	mpz_class probable_prime(num);
	auto probable_prime_res = mpz_probab_prime_p(probable_prime.get_mpz_t(), trials);
    return probable_prime_res;
}