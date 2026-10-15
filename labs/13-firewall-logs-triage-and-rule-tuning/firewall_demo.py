import csv
from io import StringIO
from collections import Counter
text="time,src,dst,port,action\n09:00,10.0.0.5,192.0.2.10,443,ALLOW\n09:01,10.0.0.5,192.0.2.20,22,DENY\n09:02,10.0.0.5,192.0.2.20,22,DENY\n09:03,10.0.0.8,192.0.2.10,443,ALLOW\n"
rows=list(csv.DictReader(StringIO(text)))
print("Decisions:",dict(Counter(r["action"] for r in rows)))
print("Denied sources:",dict(Counter(r["src"] for r in rows if r["action"]=="DENY")))
assert len(rows)==4