import requests
import pyaudio
import time
from math import log10
import audioop  
import csv
import serial
import adafruit_gps

uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')
        
        
def callback(in_data, frame_count, time_info, status):
	global rms
	rms = audioop.rms(in_data, WIDTH) / 32767
	return in_data, pyaudio.paContinue

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 0
i=0
Data=[]
energy_data=[]
lat_data=[]
long_data=[]
latitude = 42.290598
longitude = -83.713351
print(p.get_default_input_device_info())




stream = p.open(format=p.get_format_from_width(WIDTH),
				input_device_index=DEVICE,
				channels=1,
				rate=RATE,
				input=True,
				output=False,
				stream_callback=callback)

stream.start_stream()
f= open("/home/pi/Documents/Data1","w")
writer = csv.writer(f)
while stream.is_active(): 
    gps.update()
    Data.append(rms)
    i=i+1
	# refresh every x seconds 
    #time.sleep(.001)
    if i > 1000000:
        print(sum(Data))
        if gps.has_fix:
            latitude = gps.latitude
            longitude = gps.longitude
            energy_data.append(sum(Data))
            lat_data.append(latitude)
            long_data.append(longitude)
            i=0
            print(f'Lattitude: {latitude}, Longitude: {longitude}')
            if sum(Data)==0:
                stream.stop_stream()
                stream.close()
                writer.writerow([str(energy_data)])
                writer.writerow([str(lat_data)])
                writer.writerow([str(long_data)])
                f.close 
                p.terminate()
            Data=[]
        else:
            energy_data.append(sum(Data))
            lat_data.append(latitude)
            long_data.append(longitude)
            i=0
            print(f'Lattitude: {latitude}, Longitude: {longitude}')
            if sum(Data)==0:
                stream.stop_stream()
                stream.close()
                writer.writerow([str(energy_data)])
                writer.writerow([str(lat_data)])
                writer.writerow([str(long_data)])
                f.close 
                p.terminate()
            Data=[]

