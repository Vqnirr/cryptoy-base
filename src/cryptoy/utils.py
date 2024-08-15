import random
from math import ceil

def str_to_unicodes(s: str) -> list[int]:
    return [ord(char) for char in s]

def unicodes_to_str(codes: list[int]) -> str:
    return "".join([chr(code) for code in codes])

def bytes_to_binary_strings(bytes_: bytes) -> list[str]:
    return [f"{b:08b}" for b in bytes_]

def str_to_binary_strings(s: str) -> list[str]:
    return bytes_to_binary_strings(s.encode())

def concat_binary_strings(byte_strings: list[str]) -> str:
    return "".join(byte_strings)

def str_to_binary(s: str) -> str:
    return concat_binary_strings(str_to_binary_strings(s))

def str_to_int(s: str) -> int:
    return int(str_to_binary(s), 2)

def split_binary_strings(s: str) -> list[str]:
    return [s[i:i + 8] for i in range(0, len(s), 8)]

def binary_strings_to_bytes(bytes_: list[str]) -> bytes:
    return bytes([int(c, 2) for c in bytes_])

def bytes_to_str(bytes_: bytes) -> str:
    return bytes_.decode()

def int_to_binary(value: int) -> str:
    s = f"{value:b}"
    size = ceil(len(s) / 8) * 8
    return f"{s:0>{size}}"

def int_to_str(value: int) -> str:
    return bytes_to_str(binary_strings_to_bytes(split_binary_strings(int_to_binary(value))))

def pow_mod(b: int, e: int, m: int) -> int:
    if e == 0:
        return 1
    root = pow_mod(b, e // 2, m)
    return (root * root * (b if e % 2 else 1)) % m

def miller_rabin(n: int, k: int) -> bool:
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def draw_random_prime(min: int = 2**1023, max: int = 2**1024) -> int:
    while True:
        p = (2 * random.randint(min, max) + 1) % max
        if pow_mod(2, p - 1, p) == 1 and miller_rabin(p, 40):
            return p

def modular_inverse(a: int, n: int) -> int:
    t, newt, r, newr = 0, 1, n, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise RuntimeError("a not invertible")
    return t + n if t < 0 else t
