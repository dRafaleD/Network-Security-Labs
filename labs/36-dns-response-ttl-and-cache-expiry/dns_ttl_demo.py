"""Offline DNS cache TTL exercise, with synthetic timestamps."""
records = [
    {"domain":"training.example", "address":"192.0.2.10", "observed_at":100, "ttl":60},
    {"domain":"training.example", "address":"192.0.2.20", "observed_at":180, "ttl":15},
]
def valid_at(record, second):
    return record["observed_at"] <= second < record["observed_at"] + record["ttl"]
assert valid_at(records[0],159)
assert not valid_at(records[0],160)
assert valid_at(records[1],180)
assert not valid_at(records[1],195)
for record in records:
    print(record["domain"], "expires", record["observed_at"] + record["ttl"])
print("This models TTL windows, not real DNSSEC or DNS resolution.")
