from datetime import datetime,timezone
events=[("2026-10-21T09:00:00+03:00","fw-1","blocked","10.0.0.2"),("2026-10-21T06:00:00+00:00","fw-1","blocked","10.0.0.2"),("2026-10-21T06:01:00+00:00","fw-2","allowed","10.0.0.3")]
seen=set()
for ts,dev,action,src in events:
    key=(datetime.fromisoformat(ts).astimezone(timezone.utc),dev,action,src)
    if key in seen:print("duplicate",dev,src)
    else:seen.add(key);print("event",key)
