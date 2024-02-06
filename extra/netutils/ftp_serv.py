import wifi
from socketpool import SocketPool
from ftp_server import ftp
from supervisor import reload

if not wifi.radio.connected:
    print("No wifi. Trying to connect via settings.toml")

    from cptoml import keys, fetch

    stored_networks = keys("IWD")
    available_networks = []
    for i in wifi.radio.start_scanning_networks():
        available_networks.append(i.ssid)
    wifi.radio.stop_scanning_networks()
    for i in stored_networks:
        if i in available_networks:
            try:
                wifi.radio.connect(i, fetch(i, "IWD"))
                if wifi.radio.connected:
                    print("Successfully connected to " + i)
                    break
            except:
                pass

if not wifi.radio.connected:
    print("Could not connect to wifi!")
    reload()

pool = SocketPool(wifi.radio)
ftps = ftp(pool, str(wifi.radio.ipv4_address), verbose=True)
print("Starting Ljinux ftp server..")
try:
    ftps.serve_till_quit()
except KeyboardInterrupt:
    pass
finally:
    ftps.deinit()
print("Reloading Ljinux..")
reload()
