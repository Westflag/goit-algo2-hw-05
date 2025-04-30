import json
import time
from typing import Tuple
from datasketch import HyperLogLog
import pandas as pd

LOG_FILE = "lms-stage-access.log"


def load_ip_addresses(filename: str) -> list:
    ip_addresses = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                continue  # Пропускаємо некоректні рядки
    print(len(ip_addresses))
    return ip_addresses


def exact_count(ip_addresses: list) -> Tuple[int, float]:
    start = time.time()
    unique_ips = set(ip_addresses)
    end = time.time()
    return len(unique_ips), round(end - start, 4)


def approximate_count(ip_addresses: list, hll_p=0.01) -> Tuple[float, float]:
    hll = HyperLogLog(p=14)  # p=14 дає похибку ~1%
    start = time.time()
    for ip in ip_addresses:
        hll.update(ip.encode('utf-8'))
    end = time.time()
    return round(hll.count(), 2), round(end - start, 4)


def compare_methods():
    ip_addresses = load_ip_addresses(LOG_FILE)

    exact, exact_time = exact_count(ip_addresses)
    approx, approx_time = approximate_count(ip_addresses)

    df = pd.DataFrame({
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact, approx],
        "Час виконання (сек.)": [exact_time, approx_time]
    })

    print("\nРезультати порівняння:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    compare_methods()
