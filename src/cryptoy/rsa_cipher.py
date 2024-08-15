import sys
from math import gcd
from cryptoy.utils import (
    draw_random_prime,
    int_to_str,
    str_to_int,
)

sys.setrecursionlimit(5000)

def keygen() -> dict:
    e = 65537
    p = draw_random_prime()
    q = draw_random_prime()
    
    while p == q:
        q = draw_random_prime()

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    return {"public_key": (e, n), "private_key": (d, n)}

def encrypt(msg: str, public_key: tuple) -> int:
    e, n = public_key
    return pow(str_to_int(msg), e, n)

def decrypt(msg: int, private_key: tuple) -> str:
    d, n = private_key
    return int_to_str(pow(msg, d, n))
