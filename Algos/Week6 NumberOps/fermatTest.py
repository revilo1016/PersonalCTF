
import random
'''
If n is a prime number, then for every a, 1 < a < n-1,

a**(n-1) ≡ 1 (mod n)
 OR 
a**(n-1) % n = 1
'''
def power(x, y, z):
    """
    Calculate x**y%z

    :return: res
    """
    res = 1

    x = x % z

    while y > 0:

        '''
        if y is odd then multiply by x res
        '''
        if y % 2 != 0:
            res = (res * x) % z
            y = y - 1
        else:
            x = (x ** 2) % z
            '''
            this makes y even // = multiply and round
            '''
            y = y // 2

    return res % z


def isPrime(x, y):
    """
    if x is prime return true, else false
    :param x: number to test
    :param y: times to try (higher = more confidence
    :return: True or false
    """
    '''
    potential edge cases
    '''
    if x == 1 or x == 4:
        return False
    elif x == 2 or x == 3:
        return True

    else:
        '''
        if neither, try y times
        '''
        for i in range(y):

            '''
            pick our random witness
            '''
            a = random.randint(2, x - 2)

            '''
            perform fermats theorem
            '''
            if power(a, x - 1, x) != 1:
                return False

    return True