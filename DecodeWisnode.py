import serial
import time
import sys
import binascii

ser = serial.serial_for_url(str(sys.argv[1]), 115200)
try:
  if ser.isOpen():
    z=ser.read_until()
    #print(z)
    while z.find(b'Initialization OK')<0:
      z=ser.read_until()
      #print(z)
  print(z)
  print("\nReady\n===========\n")
  while True:
    z=ser.read_until()
    #print(z)
    b=z.decode("utf-8").split("=")
    cmd=b[0]
    if cmd=="at+recv":
      c=b[1].split(':')
      data=c[0].split(',')
      rssi=data[0]
      snr=data[1]
      length=data[2]
      #print("Decoding "+c[1])
      msg=binascii.unhexlify(c[1].strip()).decode('utf-8')
      print("Incoming:")
      print(" . RSSI: "+rssi)
      print(" . SNR: "+snr)
      print(" . Length: "+length)
      print(" . "+msg)
      parts = msg.split(',')
      parts.reverse()
      print(" . Message ID: "+parts.pop())
      checkCode = parts.pop()
      print(" . Error code: "+checkCode)
      if checkCode == '0':
        print(" PM2.5:")
        print(" . PM1.0 concentration (CF=1, Standard particulate matter): "+parts.pop()+" ug/m3")
        print(" . PM2.5 concentration (CF=1, Standard particulate matter): "+parts.pop()+" ug/m3")
        print(" . PM10  concentration (CF=1, Standard particulate matter): "+parts.pop()+" ug/m3")
        print(" . PM1.0 concentration (CF=1, Atmospheric environment): "+parts.pop()+" ug/m3")
        print(" . PM2.5 concentration (CF=1, Atmospheric environment): "+parts.pop()+" ug/m3")
        print(" . PM10  concentration (CF=1, Atmospheric environment): "+parts.pop()+" ug/m3")
        print(" BME280:")
        print(" . Temperature: "+parts.pop()+"°C")
        print(" . Humidity: "+parts.pop()+"%")
        print(" SHT15:")
        print(" . Temperature: "+parts.pop()+"°C")
        print(" . Humidity: "+parts.pop()+"%")
      elif checkCode == '1':
        print(" GAS_GMXXX:")
        print(" . GM102B / NO2: "+parts.pop())
        print(" . GM302B / Alcohol gas: "+parts.pop())
        print(" . GM502B / VOC gas: "+parts.pop())
        print(" . GM702B / CO2: "+parts.pop())
      print("")

except serial.SerialException as e:
  print("Exception")
  sys.stderr.write('could not open port {!r}: {}\n'.format(args.port, e))
  if ser.isOpen():
    ser.close()
