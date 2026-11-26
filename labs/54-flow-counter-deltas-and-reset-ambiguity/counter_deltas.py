"""Offline cumulative telemetry arithmetic, using fictional counters only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Sample:
    origin: str
    epoch: str
    time: int
    total: int

def delta(a,b):
    if any(type(v) is not int for v in (a.time,b.time,a.total,b.total)):
        return "INVALID",None
    if min(a.total,b.total)<0:
        return "INVALID",None
    if a.origin!=b.origin:
        return "DIFFERENT_ORIGIN",None
    if b.time<=a.time:
        return "TIME_CONFLICT",None
    if a.epoch!=b.epoch:
        return "RESET_BOUNDARY",None
    if b.total<a.total:
        return "COUNTER_REGRESSION",None
    return "DELTA",b.total-a.total

def main():
    a=Sample("lab-a","boot-1",10,100)
    cases=[
        (Sample("lab-a","boot-1",20,160),("DELTA",60)),
        (Sample("lab-a","boot-1",20,100),("DELTA",0)),
        (Sample("lab-a","boot-1",20,90),("COUNTER_REGRESSION",None)),
        (Sample("lab-a","boot-2",20,5),("RESET_BOUNDARY",None)),
        (Sample("lab-a","boot-2",20,200),("RESET_BOUNDARY",None)),
        (Sample("lab-b","boot-1",20,160),("DIFFERENT_ORIGIN",None)),
        (Sample("lab-a","boot-1",10,160),("TIME_CONFLICT",None)),
        (Sample("lab-a","boot-1",9,160),("TIME_CONFLICT",None)),
        (Sample("lab-a","boot-1",20,-1),("INVALID",None)),
        (Sample("lab-a","boot-1",20,True),("INVALID",None)),
    ]
    for b,expected in cases:
        actual=delta(a,b)
        assert actual==expected,(b,actual)
        print(b,actual)
    print("10 counter scenarios passed")

if __name__=="__main__":
    main()
