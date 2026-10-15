"""Summarize harmless synthetic network flows; no packet capture."""
import csv
from collections import defaultdict
from pathlib import Path
counts=defaultdict(lambda:[0,0])
with Path(__file__).with_name("flows.csv").open(newline="",encoding="utf-8") as f:
 for row in csv.DictReader(f):
  key=(row["dst_ip"],row["dst_port"],row["protocol"])
  counts[key][0]+=1
  counts[key][1]+=int(row["bytes"])
for key,(events,bytes_) in sorted(counts.items()):
 print(key,"flows",events,"bytes",bytes_)
print("Flow statistics are not user attribution or malware evidence.")
