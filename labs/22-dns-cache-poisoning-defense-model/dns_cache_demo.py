"""Offline toy DNS cache policy; no DNS requests or cryptographic DNSSEC validation."""
from dataclasses import dataclass

MAX_TTL = 300

@dataclass(frozen=True)
class Answer:
    question: str
    address: str
    ttl: int
    validated: bool  # Simulated result from trusted upstream, not proof of DNSSEC

class Cache:
    def __init__(self):
        self.entries = {}

    def accept(self, expected: str, answer: Answer, now: int) -> bool:
        if answer.question != expected or not answer.validated or not 0 < answer.ttl <= MAX_TTL:
            return False
        self.entries[expected] = (answer.address, now + answer.ttl)
        return True

    def get(self, name: str, now: int):
        item = self.entries.get(name)
        if item is None:
            return None
        addr, expiry = item
        if now >= expiry:
            del self.entries[name]
            return None
        return addr

cache = Cache()
good = Answer("training.example", "192.0.2.10", 60, True)
unverified = Answer("training.example", "192.0.2.99", 600, False)
wrong_name = Answer("other.example", "192.0.2.20", 60, True)
assert cache.accept("training.example", good, now=100)
assert not cache.accept("training.example", unverified, now=110)
assert not cache.accept("training.example", wrong_name, now=110)
assert cache.get("training.example", 159) == "192.0.2.10"
assert cache.get("training.example", 160) is None
print("Cache trust and expiry checks passed (synthetic only).")
