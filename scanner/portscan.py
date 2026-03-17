import socket

def port_scan(hostname):
    ports = [21, 22, 80, 443, 3306]
    open_ports = []
    for p in ports:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((hostname, p))
            open_ports.append(p)
            s.close()
        except:
            pass
    return open_ports
