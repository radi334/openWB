#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
ipaddress = str(sys.argv[1])
slave1id = int(sys.argv[2])
slave2id = int(sys.argv[3])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)

#wr1
resp= client.read_holding_registers(40084,2,unit=slave1id)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

respw= client.read_holding_registers(40083,2,unit=slave1id)
value1w = respw.registers[0]
allw = format(value1w, '04x')
rawprodw = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
if fmultiplint == 0:
    rawprodw = rawprodw
if fmultiplint == -1:
    rawprodw = rawprodw / 10 
if fmultiplint == -2:
    rawprodw = rawprodw / 100
if fmultiplint == -3:
    rawprodw = rawprodw / 1000
if fmultiplint == -4:
    rawprodw = rawprodw / 10000

resp= client.read_holding_registers(40093,2,unit=slave1id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])

#wr2
resp= client.read_holding_registers(40084,2,unit=slave2id)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

respw= client.read_holding_registers(40083,2,unit=slave2id)
value1w = respw.registers[0]
allw = format(value1w, '04x')
rawprod2w = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
if fmultiplint == 0:
    rawprod2w = rawprod2w
if fmultiplint == -1:
    rawprod2w = rawprod2w / 10 
if fmultiplint == -2:
    rawprod2w = rawprod2w / 100
if fmultiplint == -3:
    rawprod2w = rawprod2w / 1000
if fmultiplint == -4:
    rawprod2w = rawprod2w / 10000
realrawprodw = rawprodw + rawprod2w
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(realrawprodw))
f.close()

resp= client.read_holding_registers(40093,2,unit=slave2id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final2 = int(struct.unpack('>i', all.decode('hex'))[0])
rfinal = final + final2
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(rfinal))
f.close()
pvkwhk= rfinal / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()




