from datetime import datetime,timedelta,timezone
firewall=datetime.fromisoformat('2026-10-18T10:00:00+00:00')
ids=datetime.fromisoformat('2026-10-18T10:02:30+00:00')
offset=timedelta(minutes=2,seconds=30)
print('observed delta seconds:',(ids-firewall).total_seconds())
print('after verified clock correction:',(ids-offset-firewall).total_seconds())
print('Do not assume the offset without an independent time reference.')
