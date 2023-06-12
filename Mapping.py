import requests
import pyaudio
import time
from math import log10
import audioop  
import csv


def get_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    data = response.json()
    
    if 'loc' in data:
        latitude, longitude = data['loc'].split(',')
        return float(latitude), float(longitude)
    else:
        return None
        
def callback(in_data, frame_count, time_info, status):
	global rms
	rms = audioop.rms(in_data, WIDTH) / 32767
	return in_data, pyaudio.paContinue

location = get_location()
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
	
    Data.append(rms)
    i=i+1
	# refresh every x seconds 
	#time.sleep(0.001)
    if i > 5000000:
        print(sum(Data))
        if location:
            latitude, longitude = location
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
            print('Location data not available')
        


