rules={("user","dns",53):True,("user","db",5432):False,("app","db",5432):True}
def allow(src,dst,port):return rules.get((src,dst,port),False)
for test in [("user","dns",53),("user","db",5432),("app","db",5432),("guest","db",5432)]:
    print(test,"ALLOW" if allow(*test) else "DENY")
