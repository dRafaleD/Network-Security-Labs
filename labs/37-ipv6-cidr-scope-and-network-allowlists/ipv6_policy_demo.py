"""Offline IPv6 source allowlist. No network calls or firewall changes."""
from ipaddress import ip_address, ip_network, IPv6Address

ALLOWED_V6 = ip_network("2001:db8:10::/64")
ALLOWED_PORT = 443

def may_connect(source: str, port: int, protocol: str = "tcp") -> bool:
    addr = ip_address(source)
    return (isinstance(addr, IPv6Address)
            and addr in ALLOWED_V6
            and port == ALLOWED_PORT
            and protocol.lower() == "tcp")

cases = [
    ("2001:db8:10::10", 443, True),
    ("2001:db8:10:0:ffff::1", 443, True),
    ("2001:db8:11::10", 443, False),
    ("fe80::1", 443, False),
    ("2001:db8:10::10", 22, False),
    ("192.0.2.20", 443, False),
]
for address, port, expected in cases:
    actual = may_connect(address, port)
    print(f"{address} port={port}: {'ALLOW' if actual else 'DENY'}")
    assert actual is expected

assert ALLOWED_V6.prefixlen == 64
print("6/6 synthetic policy cases passed.")
