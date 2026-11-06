"""Classify synthetic MAC addresses by OUI table and the locally-administered bit."""
OUI = {"00:50:56": "VirtualVendorA", "3c:22:fb": "LaptopVendorB"}


def classify(mac):
    octets = mac.lower().split(":")
    first = int(octets[0], 16)
    locally_administered = bool(first & 0b10)
    multicast = bool(first & 0b01)
    vendor = OUI.get(":".join(octets[:3]), "unknown")
    return {"vendor": vendor, "locally_administered": locally_administered, "multicast": multicast}


if __name__ == "__main__":
    macs = ["00:50:56:aa:bb:cc", "3c:22:fb:01:02:03", "da:a1:19:44:55:66", "01:00:5e:00:00:fb"]
    for m in macs:
        print(m, classify(m))
    assert classify(macs[0])["vendor"] == "VirtualVendorA" and not classify(macs[0])["locally_administered"]
    assert classify(macs[2])["locally_administered"] and classify(macs[2])["vendor"] == "unknown"
    assert classify(macs[3])["multicast"]
    print("PASS: vendor labels come from the OUI and randomized addresses show the local bit.")
    print("Review: a MAC address is a label that anyone can set, not proof of identity.")
