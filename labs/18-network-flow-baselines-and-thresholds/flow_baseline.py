from statistics import median
baseline=[12,14,13,15,12,14,13]
current=[13,14,52,15]
threshold=median(baseline)*3
print("baseline median",median(baseline),"threshold",threshold)
for n in current:print(n,"REVIEW" if n>threshold else "normal")
