def decomp(n):
    global prime_dict
    prime_dict = {}
    global primes
    primes = prime_sieve(n)
    for i in primes:
        prime_dict[i] = 0
    for i in range(2, n + 1):
        if i in primes:
            prime_dict[i] += 1
        else:
            factorise(i)
    factors = []
    for key in sorted(prime_dict.keys()):
        if prime_dict[key] != 0:
            if prime_dict[key] != 1:
                factors.append("%s^%s" % (key, prime_dict[key]))
            else:
                factors.append(str(key))

    return (" * ".join(factors))


def prime_sieve(n):
    x = list(range(n + 1))
    for i in range(2, n + 1):
        divisor = i
        while divisor + i < n + 1:
            divisor += i
            x[divisor] = False
    x = [i for i in x if i != False]
    return x[1:]


def factorise(n):
    for i in primes:
        counter = 0
        if i <= n:
            if n % i == 0:
                while n % i == 0:
                    n /= i
                    counter += 1
                prime_dict[i] += counter
