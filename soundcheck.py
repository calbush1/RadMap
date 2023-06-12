import pyaudio
import time
from math import log10
import audioop  
import csv



p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 0
i=0
Data=[]
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
	global rms
	rms = audioop.rms(in_data, WIDTH) / 32767
	return in_data, pyaudio.paContinue


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
		stream.stop_stream()
		stream.close()
		#writer.writerow([str(Data)])
		f.close 
		p.terminate()
