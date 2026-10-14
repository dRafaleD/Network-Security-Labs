#!/usr/bin/env python3
"""Explainable synthetic DNS baseline analysis. Not a malware detector."""
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json
import sys

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("synthetic_dns.jsonl")
events=defaultdict(list)
for line_no,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
    if not line.strip():continue
    e=json.loads(line)
    if not {"timestamp","client","qname","rcode"}<=e.keys():
        raise ValueError(f"missing field at {line_no}")
    e["parsed_time"]=datetime.fromisoformat(e["timestamp"])
    if e["parsed_time"].utcoffset() is None:
        raise ValueError(f"timestamp lacks timezone at line {line_no}")
    events[e["client"]].append(e)

for client,items in sorted(events.items()):
    items.sort(key=lambda e:e["parsed_time"])
    total=len(items)
    missing=sum(e["rcode"]=="NXDOMAIN" for e in items)
    ratio=missing/total
    # Count NXDOMAIN inside any inclusive 2-minute window.
    nxd=[e["parsed_time"] for e in items if e["rcode"]=="NXDOMAIN"]
    max_burst=0
    left=0
    for right,t in enumerate(nxd):
        while (t-nxd[left]).total_seconds()>120:
            left+=1
        max_burst=max(max_burst,right-left+1)
    notes=[]
    if total>=10 and ratio>=0.5: notes.append("elevated NXDOMAIN proportion")
    if max_burst>=8:notes.append("NXDOMAIN burst within 2 minutes")
    # Informative only; periodicity analysis needs proper window/context.
    print(f"{client}: queries={total}, NXDOMAIN={missing}, ratio={ratio:.1%}, "
          f"largest_2min_burst={max_burst}")
    print("  triage signals:", ", ".join(notes) if notes else "none by toy thresholds")
    print("  NOTE: signals are not verdicts; compare with DHCP, resolver, asset and app logs.")
