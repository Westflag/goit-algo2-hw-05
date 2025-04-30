import hashlib
from typing import List, Dict

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str) -> List[int]:
        hashes = []
        for i in range(self.num_hashes):
            hash_input = f"{i}-{item}".encode('utf-8')
            hash_digest = hashlib.md5(hash_input).hexdigest()
            hash_value = int(hash_digest, 16) % self.size
            hashes.append(hash_value)
        return hashes

    def add(self, item: str):
        if not isinstance(item, str):
            return
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            return False
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: List[str]) -> Dict[str, str]:
    results = {}
    for pwd in passwords:
        if not isinstance(pwd, str) or pwd == "":
            results[pwd] = "некоректне значення"
        elif pwd in bloom_filter:
            results[pwd] = "вже використаний"
        else:
            results[pwd] = "унікальний"
            bloom_filter.add(pwd)
    return results

# Приклад використання
if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
