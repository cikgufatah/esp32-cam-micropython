from machine import Pin
import os, network, machine
import wifimgr
import picoweb
import camera
import ntptime
import dht
import gc

gc.collect()

#sd = machine.SDCard(slot=0 width=4)
#os.mount(sd, '/sd')


light = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
temp = dht.DHT11(Pin(14))

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass

print("ESP OK")

ntptime.settime()
camera.init(0, format=camera.JPEG)
app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type='text/html')
    yield from resp.awrite("<html><title>Fatah's ESP</title><body><center><h1>Fatah's ESP</h1></center></body></html>")

@app.route("/capture/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type='image/jpeg')
    yield from resp.awrite(camera.capture())

@app.route("/sensor/")
def index(req, resp):
    temp.measure()
    yield from picoweb.start_response(resp, content_type='application/json')
    yield from resp.awrite('{"light":'+str(light.value())+',"temperature":'+str(temp.temperature())+',"humidity":'+str(temp.humidity())+'}')

app.run(debug=False, host='0.0.0.0', port=80)
