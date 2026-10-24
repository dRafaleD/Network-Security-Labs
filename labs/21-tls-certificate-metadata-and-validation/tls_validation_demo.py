"""Toy TLS certificate validation model; not a real TLS implementation."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class CertificateFacts:
    hostname_matches: bool
    chain_trusted: bool
    not_before: datetime
    not_after: datetime

def validate(facts: CertificateFacts, now: datetime) -> dict[str, bool]:
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    now = now.astimezone(timezone.utc)
    return {
        "hostname_matches": facts.hostname_matches,
        "chain_trusted": facts.chain_trusted,
        "within_validity_period": facts.not_before <= now <= facts.not_after,
    }

if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    facts = CertificateFacts(
        hostname_matches=True,
        chain_trusted=True,
        not_before=datetime(2020, 1, 1, tzinfo=timezone.utc),
        not_after=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )
    results = validate(facts, now)
    for check, passed in results.items():
        print(f"{check}: {'PASS' if passed else 'FAIL'}")
    print("Overall model result:", "PASS" if all(results.values()) else "FAIL")
    print("Educational model only; it does not parse or verify real certificates.")
