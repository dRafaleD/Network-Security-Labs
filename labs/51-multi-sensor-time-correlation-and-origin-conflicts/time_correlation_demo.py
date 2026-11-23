#!/usr/bin/env python3
"""Toy authenticated IPv6 sensor correlation with clock disagreement."""
from hashlib import sha256
import hmac
import json

KEYS = {"sensor-a": b"public-a-key", "sensor-b": b"public-b-key"}
COLLECTORS = {"a-direct":"sensor-a","a-relay":"sensor-a",
              "b-direct":"sensor-b"}
ACTIVE = {"sensor-a","sensor-b"}
WINDOW = 2

def canonical(data):
    return json.dumps(data,sort_keys=True,separators=(",",":")).encode()

def issue(sensor, event="DAD_FAIL", time=100, address="2001:db8::7"):
    fields={"sensor":sensor,"event":event,"time":time,
            "address":address,"boot":"epoch-2"}
    return {**fields,"tag":hmac.new(KEYS[sensor],canonical(fields),sha256).hexdigest()}

def trusted(collector, record):
    sensor=COLLECTORS.get(collector)
    if sensor not in ACTIVE or not isinstance(record,dict):
        return False
    try:
        payload={key:record[key] for key in ("sensor","event","time","address","boot")}
        if payload["sensor"]!=sensor or type(payload["time"]) is not int:
            return False
        if not isinstance(record["tag"],str):
            return False
        expected=hmac.new(KEYS[sensor],canonical(payload),sha256).hexdigest()
        return hmac.compare_digest(record["tag"],expected)
    except (KeyError,TypeError,ValueError):
        return False

def correlate(records):
    by_sensor={}
    for collector,record in records:
        if not trusted(collector,record):
            continue
        sensor=COLLECTORS[collector]
        by_sensor.setdefault(sensor,set()).add(
            (record["event"],record["address"],record["time"]))
    if not by_sensor:
        return "NO_TRUSTED_EVIDENCE"
    if any(len(items)>1 for items in by_sensor.values()):
        return "ORIGIN_CONFLICT"
    events=[next(iter(items)) for items in by_sensor.values()]
    if len({(event,addr) for event,addr,_ in events})>1:
        return "CROSS_SENSOR_CONFLICT"
    if max(item[2] for item in events)-min(item[2] for item in events)>WINDOW:
        return "TIME_DISAGREEMENT"
    return "CORROBORATED_CONTEXT" if len(by_sensor)>1 else "SINGLE_ORIGIN"

def main():
    a,b=issue("sensor-a"),issue("sensor-b",time=101)
    cases=[
        ("single origin",[("a-direct",a)],"SINGLE_ORIGIN"),
        ("forwarded copy",[("a-direct",a),("a-relay",a)],"SINGLE_ORIGIN"),
        ("two near-time sources",[("a-direct",a),("b-direct",b)],"CORROBORATED_CONTEXT"),
        ("timestamps far apart",[("a-direct",a),("b-direct",issue("sensor-b",time=106))],"TIME_DISAGREEMENT"),
        ("sensor status conflicts",[("a-direct",a),("b-direct",issue("sensor-b",event="DAD_OK"))],"CROSS_SENSOR_CONFLICT"),
        ("one origin changes story",[("a-direct",a),("a-relay",issue("sensor-a",time=102))],"ORIGIN_CONFLICT"),
        ("unsigned alteration",[("a-direct",{**a,"event":"DAD_OK"})],"NO_TRUSTED_EVIDENCE"),
        ("unknown collector",[("unknown",a)],"NO_TRUSTED_EVIDENCE"),
    ]
    for label,rows,expected in cases:
        result=correlate(rows)
        assert result==expected,(label,result)
        print(f"{label:33} {result}")
    ACTIVE.remove("sensor-a")
    assert correlate([("a-direct",a),("b-direct",b)])=="SINGLE_ORIGIN"
    assert correlate([("a-direct",a)])=="NO_TRUSTED_EVIDENCE"
    print(f"{len(cases)+2}/{len(cases)+2} synthetic event correlation checks passed")

if __name__=="__main__":
    main()
