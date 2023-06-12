import serial

# Open the serial connection
ser = serial.Serial('/dev/serial1', baudrate=9600, timeout=1)

# Read and print GPS data
while True:
    line = ser.readline().decode('utf-8').strip()
    #if line.startswith('$GPGGA'):
    print(line)

# Close the serial connection
ser.close()
