import wifi
from socketpool import SocketPool
from ftp_server import ftp
from supervisor import reload

if not wifi.radio.connected:
    print("No wifi")
    reload()

pool = SocketPool(wifi.radio)
ftps = ftp(pool, str(wifi.radio.ipv4_address))
print("Starting Ljinux ftp server..")
try:
    ftps.serve_till_quit()
except KeyboardInterrupt:
    pass
finally:
    ftps.deinit()
print("Reloading Ljinux..")
reload()
