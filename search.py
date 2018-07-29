import cython.primality as primality
import os
import multiprocessing as mp
import generate as gen


# CPU_COUNT = mp.cpu_count()
CPU_COUNT = 4


def get_batches(data):
    length = len(data)
    return [data[i*length // CPU_COUNT: (i+1)*length // CPU_COUNT] for i in range(CPU_COUNT)]


def search_prime(img_path):
    candidates_bytes = gen.get_candidates(img_path)
    candidates = [''.join(str(b) for b in num_bytes[::2]) for num_bytes in candidates_bytes]
    batches = [batch for batch in get_batches(candidates)]

    print('pool starting...')
    with mp.Pool(processes=CPU_COUNT) as pool:
        results = [pool.apply_async(_search_candidates, args=(batch,)) for batch in batches]
        return [res.get() for res in results]


def _search_candidates(prime_candidates):
    pid = os.getpid()
    counter = 0

    for candidate in prime_candidates:
        counter += 1
        possible_prime = primality.is_prime(candidate, 1)

        if possible_prime != 0:
            print(f'PID:{pid}, PRIME FOUND: {candidate}', flush=True)

            with open(f'{pid}_prime.txt', 'a') as f:
                f.write(f'{candidate}\n')

            return candidate

        if counter % 25 == 0:
            print(f'PID:{pid}, finished numbers:{counter}', flush=True)


if __name__ == "__main__":
    primes = search_prime(r'pic_128.jpg')
    print(primes)
