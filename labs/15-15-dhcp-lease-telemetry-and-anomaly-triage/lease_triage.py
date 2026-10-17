from collections import defaultdict
events=[
    ("2026-10-17T10:00:00","02:00:00:00:00:01","192.0.2.10","dhcp-a"),
    ("2026-10-17T10:05:00","02:00:00:00:00:02","192.0.2.11","dhcp-a"),
    ("2026-10-17T10:10:00","02:00:00:00:00:01","192.0.2.10","dhcp-b"),
]
servers=defaultdict(set)
for timestamp,mac,ip,server in events:
    servers[(mac,ip)].add(server)
for key,seen in servers.items():
    print(key,"servers:",sorted(seen),"REVIEW" if len(seen)>1 else "baseline")
print("Review does not prove a rogue server.")
