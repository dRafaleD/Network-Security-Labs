from collections import defaultdict
events=[('10.1.1.8','02:00:00:00:00:08'),('10.1.1.9','02:00:00:00:00:09'),('10.1.1.8','02:00:00:00:00:18')]
seen=defaultdict(set)
for ip,mac in events: seen[ip].add(mac)
for ip,macs in sorted(seen.items()): print(ip,sorted(macs),'REVIEW' if len(macs)>1 else 'baseline')
