"""Inspect invented network flow summaries; no sockets or packet capture."""
from dataclasses import dataclass
from ipaddress import ip_address, ip_network

LAB = ip_network("192.0.2.0/24")
PEER = ip_network("198.51.100.0/24")

@dataclass(frozen=True)
class Flow:
    ident: str
    src: str
    dst: str
    proto: str
    packets: int
    size: int

def assess(flow):
    try:
        src,dst=ip_address(flow.src),ip_address(flow.dst)
    except ValueError:
        return "INVALID_ADDRESS"
    if flow.proto not in {"TCP","UDP","ICMP"}:
        return "INVALID_PROTOCOL"
    if type(flow.packets) is not int or type(flow.size) is not int:
        return "INVALID_COUNTER"
    if flow.packets<0 or flow.size<0 or (flow.packets==0 and flow.size!=0):
        return "INVALID_COUNTER"
    if src not in LAB and src not in PEER:
        return "OUTSIDE_FIXTURE"
    if dst not in LAB and dst not in PEER:
        return "OUTSIDE_FIXTURE"
    if flow.packets==0:
        return "EMPTY_FLOW"
    if src in LAB and dst in LAB:
        return "LAB_INTERNAL"
    if src in LAB and dst in PEER:
        return "LAB_OUTBOUND"
    if src in PEER and dst in LAB:
        return "LAB_INBOUND"
    return "PEER_INTERNAL"

def main():
    cases=[
        (Flow("1","192.0.2.1","192.0.2.2","TCP",2,100),"LAB_INTERNAL"),
        (Flow("2","192.0.2.1","198.51.100.2","UDP",4,200),"LAB_OUTBOUND"),
        (Flow("3","198.51.100.2","192.0.2.1","TCP",3,150),"LAB_INBOUND"),
        (Flow("4","198.51.100.2","198.51.100.3","ICMP",1,80),"PEER_INTERNAL"),
        (Flow("5","192.0.2.1","192.0.2.2","UDP",0,0),"EMPTY_FLOW"),
        (Flow("6","192.0.2.1","192.0.2.2","TCP",0,100),"INVALID_COUNTER"),
        (Flow("7","192.0.2.1","192.0.2.2","TCP",-1,100),"INVALID_COUNTER"),
        (Flow("8","192.0.2.1","192.0.2.2","TCP",1,-1),"INVALID_COUNTER"),
        (Flow("9","invalid","192.0.2.2","TCP",1,40),"INVALID_ADDRESS"),
        (Flow("10","192.0.2.1","203.0.113.2","TCP",1,40),"OUTSIDE_FIXTURE"),
        (Flow("11","192.0.2.1","192.0.2.2","OTHER",1,40),"INVALID_PROTOCOL"),
        (Flow("12","192.0.2.1","192.0.2.2","TCP",True,40),"INVALID_COUNTER"),
    ]
    totals={}
    for flow,expected in cases:
        actual=assess(flow)
        assert actual==expected,(flow,actual)
        print(f"{flow.ident:>2} {actual}")
        if actual.startswith("LAB_") or actual=="PEER_INTERNAL":
            totals[actual]=totals.get(actual,0)+flow.size
    assert totals=={"LAB_INTERNAL":100,"LAB_OUTBOUND":200,
                    "LAB_INBOUND":150,"PEER_INTERNAL":80}
    print("Accepted byte totals:",totals)
    print("12 flows + 1 aggregate check passed")

if __name__=="__main__":
    main()
