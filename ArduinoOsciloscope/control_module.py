#MIT License
#
#Copyright (c) 2024 Luis Victor Muller Fabris
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import time
import random
import sys
import os
from spectrareadapi import setxdata, setydata, seterr, setwarning, setinfo, pushval, setxlabel, setylabel, npushval

import serial
from struct import unpack

i=0
stream=None

i=0
okgeneric=1
tryagain=1
oldpar=None
contstate=0
def mainloop(meas,single,par):
	timeaa=time.time()
	global multiproccessingpool
	global mmapb
	global mmapc
	global mmapd
	global queue
	global timelastcal
	global strxdata
	global lastsingle
	global connectedfinal
	global instid
	global mmaperror
	global errorcurrent
	global x
	global i
	global stream
	global serial
	global okgeneric
	global tryagain
	global oldpar
	global contstate
	setinfo(" ")
	setxlabel("x")
	setylabel("y")
	parb=par[2].split(" ")
	#print par
	#print "meas:"+str(meas)+" single:"+str(single)+" par:"+str(par)
	if(meas==True) or (single==True):
		try:
			if(tryagain==1):
				if(stream==None):
					print "Open a"
					contstate=0
					oldpar=None
					stream=serial.Serial( '/dev/ttyACM0', 1000000, timeout=0.5, write_timeout=0.2, inter_byte_timeout=0.2, exclusive=1 )  # open first serial port
					stream.flushOutput()
					stream.flushInput()
					stream.write(b'\ns\n')
					stream.write(b'\ns\n')
					time.sleep(0.1)
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
				if(stream.isOpen() == False):
					print "Open b"
					contstate=0
					oldpar=None
					stream=serial.Serial( '/dev/ttyACM0', 1000000, timeout=0.5, write_timeout=0.2, inter_byte_timeout=0.2, exclusive=1 )  # open first serial port
					stream.flushOutput()
					stream.flushInput()
					stream.write(b'\ns\n')
					stream.write(b'\ns\n')
					time.sleep(0.1)
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
					stream.write(b'\ns\n')
					null=(stream.readline())
				okgeneric=1
		except:
			pass
		try:
			if(stream==None):
				if(okgeneric==1):
					seterr("USB Device not found")
				okgeneric=0
			if(stream.isOpen() == False):
				if(okgeneric==1):
					seterr("USB Device not found")
				okgeneric=0
		except:
			pass
		#print("1 %s s" % str(time.time()-timeaa))
		try:
			if(okgeneric==1):
				if(par!=oldpar):
					stream.flushOutput()
					stream.flushInput()
					prescaler=('p'+str(par[0])+'\n')
					stream.write(prescaler)
					#null=(stream.readline())
					#print null
					#if(null==""):
					#	raise Exception(" ")
					trigger='t'+str((parb[1]))+'\n'
					stream.write(trigger)
					#null=(stream.readline())
					#print null
					#if(null==""):
					#	raise Exception(" ")
					previouspoints='b'+str((parb[2]))+'\n'
					stream.write(previouspoints)
					#null=(stream.readline())
					#print null
					#if(null==""):
					#	raise Exception(" ")
					afterpoints='n'+str((parb[3]))+'\n'
					stream.write(afterpoints)
					trigmode='m '+str((par[1]))+'\n'
					stream.write(trigmode)
					print trigmode
					#null=(stream.readline())
					#print null
					#if(null==""):
					#	raise Exception(" ")
					#stream.write(b's')
				if(single==True):
					stream.write(b'\ns\n')
					print "Single"
					#null=(stream.readline())
					#print null
				else:
					if(contstate==0):
						stream.write(b'\nc\n')
						print "continuous"
						contstate=1
					#null=(stream.readline())
					#print null
				#print("2 %s s" % str(time.time()-timeaa))
				oldpar=par
				print "read"
				null=(stream.readline())
				#print("3 %s s" % str(time.time()-timeaa))
				#print null
				if("Data:" in null):
					lenmeasnow=int(null.split("Data:")[1].split("\r\n")[0])
					myprescaler=(stream.readline()) ###XXX TODO This is the aquired prescaler, use this to calculate x axis for current plot in seconds
					print "prescaler:"+str(myprescaler)
					#print "Decoded len:"+str(lenmeasnow)
					eventString = stream.read(lenmeasnow*2)
					#print("4 %s s" % str(time.time()-timeaa))
					print len(eventString)
					eventData=' '.join(map(str,((unpack( str(str(lenmeasnow)+'H'), eventString )))))
					#print(x)
					#stream.write(b'S')
					#print x
					x=""
					i=0
					while(i<(lenmeasnow-1)):
						x=x+str(i+1)+" "
						i=i+1
					x=x+str(i+1)
					setxdata(x)
					setydata(eventData)
					i=i+1
					print("5 %s s" % str(time.time()-timeaa))
					if(i>9):
						i=0
					#print "sleep0.001"
					#time.sleep(0.001)
					okgeneric=1
					return pushval()
				return npushval()
			print "npush"
			return npushval()
		except Exception as errorsr:
			tryagain=0
			print "Error read"
			print errorsr
			if(okgeneric==1):
				seterr("USB IO error")
				contstate=0
			okgeneric=0
			try:
				stream.flushOutput()
				stream.flushInput()
			except:
				pass
			try:
				stream.close()
			except:
				pass
			stream=None
			time.sleep(0.3)
			return npushval()
	else:
		try:
			stream.write(b'i')
			contstate=0
			print "stop"
			#null=(stream.readline())
			#print null
		except:
			pass
		tryagain=1
		okgeneric=1
		print "sleep0.3"
		time.sleep(0.3)
		return npushval()
def load(instidb,devidfinal):
	global mmapb
	global mmapc
	global mmapd
	global p2
	global instid
	global mmaperror
	global mutex
	instid=instidb
	print("Debug:Loading demo control module"+str(devidfinal))
def unload(instid):
	global p2
	print("Debug:Unloading demo control module")
