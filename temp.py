#!/usr/bin/python3

import Adafruit_DHT as dht
import time

while True:
	h,t = dht.read_retry(dht.DHT22, 5)
	t = 1.8 * t + 28
	print('\rTemp={0:0.1f}°  Humidity={1:0.1f}%'.format(t, h), end =" ")
	time.sleep(1)
