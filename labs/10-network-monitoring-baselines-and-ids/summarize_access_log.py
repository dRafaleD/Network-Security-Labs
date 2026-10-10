"""Summarize a simple local server access log; never infer maliciousness from one line."""
from collections import Counter
from pathlib import Path
import re
import sys

pattern = re.compile(r'^([^ ]+) - - \[[^]]+\] "([A-Z]+) ([^ ]+) HTTP/[^"]+" (\d{3}) ')
path = Path(sys.argv[1]) if len(sys.argv)>1 else Path("sample_access.log")
counts = Counter()
paths = Counter()
unparsed = 0
for line in path.read_text(encoding="utf-8").splitlines():
    match = pattern.match(line)
    if not match:
        unparsed += 1
        continue
    ip, method, urlpath, status = match.groups()
    counts[(method, status)] += 1
    paths[urlpath] += 1

print("Method / status counts")
for pair, count in sorted(counts.items()):
    print(pair, count)
print("\nPaths")
for item, count in paths.most_common():
    print(item, count)
print("Unparsed records:", unparsed)
