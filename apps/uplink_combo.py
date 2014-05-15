import serial
from serial.tools import list_ports
import os
from optparse import OptionParser
import io
import time
import random
import sys
import string
import serial
import array
import xmlrpclib
import math
import socket
import numpy

DATARATE = 256
CMDLEN = 61

class socket_cmd():
    def __init__(self,cmd_host,cmd_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((cmd_host, int(cmd_port)))
    
    def send_cmd(self,cmd):
        #prepend leading 0s
        #cmd = [0x55,0xFF,0x55]
        cmd = array.array('B',cmd)
        cmd_len = len(cmd)
        
        len_byte_3 = (cmd_len >> 24) & 0xFF
        len_byte_2 = (cmd_len >> 16) & 0xFF
        len_byte_1 = (cmd_len >> 8) & 0xFF
        len_byte_0 = (cmd_len >> 0) & 0xFF
    
        header = array.array('B',[0x55] + [len_byte_3,len_byte_2,len_byte_1,len_byte_0])
        self.s.send(header)
        self.s.send(cmd)
        
class xmlrpc_client():
    def __init__(self,host,port):
        try:
            self.xml_server = xmlrpclib.Server("http://"+host+":"+str(port))
            
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
        print "Connected to XMLRPC Server"
                
    def set_freq(self,freq):
        try:
            self.xml_server.set_doppler(freq)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
    def set_invert(self,invert):
        try:
            self.xml_server.set_invert(invert)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

def main():
    
    parser = OptionParser()
    parser.add_option("-s", "--start-freq",dest="start_freq", action="store", help="Start of frequency sweep")
    parser.add_option("-q", "--stop-freq",dest="stop_freq", action="store", help="Stop of frequency sweep")
    parser.add_option("-i", "--step-freq",dest="step_freq", action="store", help="Step of frequency sweep")
    parser.add_option("-e", "--preamble-length",dest="preamble_length", action="store", help="Number of leading 0s before command is transmitted")
    parser.add_option("-p", "--cmd-port",dest="cmd_port", action="store", help="CMD Host Port")
    parser.add_option("-a", "--cmd-host",dest="cmd_host", action="store", help="CMD Host Address")
    parser.add_option("-x", "--xml-host",dest="xml_host", action="store", help="XML Host address")
    parser.add_option("-y", "--xml-port",dest="xml_port", action="store", help="XML Host Port")
    parser.add_option("-t", "--interval",dest="interval", action="store", help="Time between commands. (seconds)")
    parser.add_option("-d", "--duration",dest="test_duration", action="store", help="Total time to run test (seconds)")

    (options, args) = parser.parse_args()
    
    ctrl_client = xmlrpc_client(options.xml_host,options.xml_port)
    cmd_client = socket_cmd(options.cmd_host,options.cmd_port)
    
    stop_freq = float(options.stop_freq)
    start_freq = float(options.start_freq)
    step_freq = float(options.step_freq)
    interval = float(options.interval)
    
    preamble_length = int(options.preamble_length)
    if ( ( preamble_length + 1 + CMDLEN)/ DATARATE > interval):
        print "WARNING WARNING WARNING: Interval %f too short for uplink packet with %d bits (including preamble)." % (interval,preamble_length + 1 + 61) 
        time.sleep(5) 
    
    points = math.floor((stop_freq - start_freq)/step_freq)
    time_to_finish = points * interval
    
    print "Starting frequency sweep test with %d points.  Will take %f minutes" % (points,time_to_finish/60.0)
    

        
    current_freq = start_freq
    start_time = time.time()
    
    #TODO pull a real array from somplace useful
    cmd = [1,1,1,0,1]
    uplink_frame = numpy.array([0] * preamble_length + [1] + cmd)
    print uplink_frame
    invert = 1
    
    while(1):
        cmd_client.send_cmd(uplink_frame)
        time.sleep(interval)
        print "Sent cmd at %f with polarity %d at %f."   % (current_freq,invert,time.time())
        
        if(invert==-1):
            ctrl_client.set_freq(current_freq)
            current_freq += step_freq
            if (current_freq > stop_freq):
                print "Frequency rollover."
                current_freq = start_freq
        
        invert *= -1 
        ctrl_client.set_invert(invert)
            
        
    ctrl_client.set_freq(0)
if __name__ == '__main__':
    main()
