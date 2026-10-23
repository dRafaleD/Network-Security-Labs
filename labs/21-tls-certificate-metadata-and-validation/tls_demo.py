from datetime import datetime,timedelta,timezone
def valid(now,not_before,not_after,hostname_ok,chain_ok):
    return not_before<=now<=not_after and hostname_ok and chain_ok
now=datetime.now(timezone.utc)
print("valid",valid(now,now-timedelta(days=1),now+timedelta(days=7),True,True))
print("expired",valid(now,now-timedelta(days=9),now-timedelta(days=1),True,True))
print("hostname mismatch",valid(now,now-timedelta(days=1),now+timedelta(days=7),False,True))
