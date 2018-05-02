#include <iostream>
#include <vector>
#include <thread>
#include <fstream>
#include "mpirxx.h"
#include "mpir.h"
#include "search.h"

#define THREAD_COUNT 6

int main()
{
	std::vector<mpz_class> batches[THREAD_COUNT];
	std::vector<std::thread> threads;
	int idx = 0;
	mpz_class prime;
	std::ifstream infile("prime_candidates.txt");
	while (infile >> prime)
	{
		batches[++idx % THREAD_COUNT].emplace_back(prime);
	}
	std::cout << "dataset ready\n";
	

	for (int i = 0; i < THREAD_COUNT; ++i)
	{
		threads.emplace_back(std::thread(calc, std::ref(batches[i]), i));
	}
	std::for_each(threads.begin(), threads.end(), std::mem_fn(&std::thread::join));
}
