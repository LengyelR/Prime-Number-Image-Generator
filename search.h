#pragma once
#include <vector>

#include "mpirxx.h"
#include "mpir.h"
#include "logger.h"

void calc(const std::vector<mpz_class>& dataset, const int id) {
	int counter = 0;
	logger log(id);

	for (auto &num : dataset)
	{
		auto res = mpz_probab_prime_p(num.get_mpz_t(), 5);
		if (res != 0)
		{
			log.info("PRIME: " + num.get_str() + "\n");
			return;
		}

		if (counter % 25 == 0)
		{
			log.info("counter: " + std::to_string(counter) + "\n");
		}
		counter++;
	}
	log.info("no primes were found.\n");
}

void verify()
{
	std::ifstream infile("solution.txt");
	mpz_class probable_prime;
	infile >> probable_prime;

	std::cout << probable_prime.get_str() << " is prime?\n";
	auto probable_prime_res = mpz_probab_prime_p(probable_prime.get_mpz_t(), 100);
	std::cout << "result:" << probable_prime_res << std::endl;
}