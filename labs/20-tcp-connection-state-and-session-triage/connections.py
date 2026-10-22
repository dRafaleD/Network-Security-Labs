from collections import Counter
events=[("a","SYN_SENT"),("a","ESTABLISHED"),("b","SYN_SENT"),("c","TIME_WAIT"),("b","CLOSED")]
final={}
for key,state in events:final[key]=state
print(final)
print(Counter(final.values()))
print("State snapshots are not proof of intrusion.")
