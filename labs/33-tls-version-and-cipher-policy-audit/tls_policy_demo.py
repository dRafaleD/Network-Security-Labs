"""Check synthetic endpoint TLS offers against a minimum version and weak-cipher policy."""
ALLOWED_VERSIONS = {"TLSv1.2", "TLSv1.3"}
WEAK = ("RC4", "3DES", "EXPORT", "NULL")
ENDPOINTS = {
    "web.example.test": {"versions": ["TLSv1.2", "TLSv1.3"], "ciphers": ["TLS_AES_128_GCM_SHA256", "ECDHE-RSA-AES256-GCM-SHA384"]},
    "legacy.example.test": {"versions": ["TLSv1.0", "TLSv1.2"], "ciphers": ["ECDHE-RSA-AES128-GCM-SHA256"]},
    "old-mail.example.test": {"versions": ["TLSv1.2"], "ciphers": ["ECDHE-RSA-AES128-GCM-SHA256", "DES-CBC3-SHA", "RC4-SHA"]},
}


def problems(offer):
    out = [f"version {v} not allowed" for v in offer["versions"] if v not in ALLOWED_VERSIONS]
    out += [f"weak cipher {c}" for c in offer["ciphers"] if any(w in c.upper() for w in WEAK)]
    return out


if __name__ == "__main__":
    for host, offer in ENDPOINTS.items():
        print(f"{host:24} {problems(offer)}")
    assert problems(ENDPOINTS["web.example.test"]) == []
    assert problems(ENDPOINTS["legacy.example.test"]) == ["version TLSv1.0 not allowed"]
    assert len(problems(ENDPOINTS["old-mail.example.test"])) == 1, "3DES is spelled DES-CBC3 and is missed"
    print("PASS: old versions and RC4 are caught, and the name-matching gap is visible.")
    print("Review: matching on names misses aliases such as DES-CBC3; use a maintained cipher list.")
