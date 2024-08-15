from math import gcd
from cryptoy.utils import str_to_unicodes, unicodes_to_str

def compute_permutation(a: int, b: int, n: int) -> list[int]:
    keys = compute_affine_keys(n)
    if a not in keys:
        raise RuntimeError(f"{a} not a valid key")
    return [(a * i + b) % n for i in range(n)]

def compute_inverse_permutation(a: int, b: int, n: int) -> list[int]:
    perm = compute_permutation(a, b, n)
    inverse_perm = [0] * n
    for i in range(n):
        inverse_perm[perm[i]] = i
    return inverse_perm

def encrypt(msg: str, a: int, b: int) -> str:
    perm = compute_permutation(a, b, 0x110000)
    return unicodes_to_str([perm[i] for i in str_to_unicodes(msg)])

def encrypt_optimized(msg: str, a: int, b: int) -> str:
    return unicodes_to_str([(a * i + b) % 0x110000 for i in str_to_unicodes(msg)])

def decrypt(msg: str, a: int, b: int) -> str:
    inverse_perm = compute_inverse_permutation(a, b, 0x110000)
    return unicodes_to_str([inverse_perm[i] for i in str_to_unicodes(msg)])

def decrypt_optimized(msg: str, a_inverse: int, b: int) -> str:
    return unicodes_to_str([((i - b) * a_inverse) % 0x110000 for i in str_to_unicodes(msg)])

def compute_affine_keys(n: int) -> list[int]:
    return [i for i in range(1, n) if gcd(i, n) == 1]

def compute_affine_key_inverse(a: int, affine_keys: list, n: int) -> int:
    for key in affine_keys:
        if (a * key) % n == 1:
            return key
    raise RuntimeError(f"{a} has no modular inverse")

def attack() -> tuple[str, tuple[int, int]]:
    s = "࠾ੵΚઐ௯ஹઐૡΚૡೢఊஞ௯\u0c5bૡీੵΚ៚Κஞїᣍફ௯ஞૡΚր\u05ecՊՊΚஞૡΚՊեԯՊ؇ԯրՊրր"
    b = 58
    keys = compute_affine_keys(0x110000)

    for key in range(1, 100):
        try:
            decrypted = decrypt(s, keys[key], b)
            if "bombe" in decrypted:
                return (decrypted, (keys[key], b))
        except:
            pass
    raise RuntimeError("Failed to attack")

def attack_optimized() -> tuple[str, tuple[int, int]]:
    s = (
        "જഏ൮ൈ\u0c51ܲ೩\u0c51൛൛అ౷\u0c51ܲഢൈᘝఫᘝా\u0c51\u0cfc൮ܲఅܲᘝ൮ᘝܲాᘝఫಊಝ"
        "\u0c64\u0c64ൈᘝࠖܲೖఅܲఘഏ೩ఘ\u0c51ܲ\u0c51൛൮ܲఅ\u0cfc\u0cfcඁೖᘝ\u0c51"
    )
    keys = compute_affine_keys(0x110000)

    for a in keys:
        a_inverse = compute_affine_key_inverse(a, keys, 0x110000)
        for b in range(1, 10000):
            decrypted = decrypt_optimized(s, a_inverse, b)
            if "bombe" in decrypted:
                return (decrypted, (a, b))
    raise RuntimeError("Failed to attack")
