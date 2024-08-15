import hashlib
import os
from random import Random
import names

def hash_password(password: str) -> str:
    return hashlib.sha3_256(password.encode()).hexdigest()

def random_salt() -> str:
    return bytes.hex(os.urandom(32))

def generate_users_and_password_hashes(passwords: list[str], count: int = 32) -> dict[str, str]:
    rng = Random()
    return {
        names.get_full_name(): hash_password(rng.choice(passwords))
        for _ in range(count)
    }

def attack(passwords: list[str], passwords_database: dict[str, str]) -> dict[str, str]:
    users_and_passwords = {}
    for password in passwords:
        hashed_password = hash_password(password)
        if hashed_password in passwords_database.values():
            user = list(passwords_database.keys())[list(passwords_database.values()).index(hashed_password)]
            users_and_passwords[user] = password
    return users_and_passwords

def fix(passwords: list[str], passwords_database: dict[str, str]) -> dict[str, dict[str, str]]:
    users_and_passwords = attack(passwords, passwords_database)
    new_database = {}
    for user, password in users_and_passwords.items():
        salt = random_salt()
        password_hash = hash_password(salt + password)
        new_database[user] = {
            "password_hash": password_hash,
            "password_salt": salt,
        }
    return new_database

def authenticate(user: str, password: str, new_database: dict[str, dict[str, str]]) -> bool:
    return hash_password(new_database[user]["password_salt"] + password) == new_database[user]["password_hash"]
