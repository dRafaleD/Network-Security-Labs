#!/usr/bin/env python3
"""Write synthetic DNS event data; no DNS request or network access is made."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

base=Path(__file__).resolve().parent
t0=datetime(2026,10,14,9,0,tzinfo=timezone.utc)
events=[]

def add(client,minutes,qname,rcode):
    events.append({"timestamp":(t0+timedelta(minutes=minutes)).isoformat(),
                   "client":client,"qname":qname,"qtype":"A","rcode":rcode})

# Ordinary working clients: mostly successful, a few typos.
for i in range(18):
    add("10.10.0.10",i*3,"intranet.example.test","NOERROR")
add("10.10.0.10",23,"intranet-typo.example.test","NXDOMAIN")
for i in range(9):
    add("10.10.0.20",i*6,"updates.example.test","NOERROR")
add("10.10.0.20",16,"oops.example.test","NXDOMAIN")

# Synthetic burst: interesting volume, NOT automatically malicious.
for i in range(12):
    add("10.10.0.30",30+i*0.15,f"miss-{i:02d}.example.test","NXDOMAIN")
for i in range(4):
    add("10.10.0.30",50+i,"ok.example.test","NOERROR")

# Synthetic near-periodic pattern: can reflect scheduled legitimate work.
for i in range(8):
    add("10.10.0.40",i*5,"heartbeat.example.test","NOERROR")

events.sort(key=lambda e:e["timestamp"])
out=base/"synthetic_dns.jsonl"
out.write_text("".join(json.dumps(e)+"\n" for e in events),encoding="utf-8")
print("Wrote",len(events),"synthetic DNS events to",out)
