#!/usr/bin/env python
import os, io, time, random, sys, string, serial, array, xmlrpclib, math, socket, datetime
from optparse import OptionParser
from serial.tools import list_ports
import numpy

DATARATE = 256
CMDLEN = 61

class socket_cmd():
    def __init__(self,cmd_host,cmd_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((cmd_host, int(cmd_port)))
        print "Connected to command server (input to flowgraph)."

    def send_cmd(self, cmd):
        #cmd = [0x55,0xFF,0x55]
        
        #flush = [0,1,0,1,0,1,0,1,0,1]
        #flush = [0]*10
        
        #cmd = flush + cmd + flush
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

    def set_pm(self,val):
        try:
            self.xml_server.set_pm(val)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

class log_this():
    def __init__(self, filename, time_format):
        try:
            self.logfile = open(filename, "w")
            print "Log file is open:", filename
        except:
            print "Could not open file"
            sys.exit(0)

    def log(self, log_str, time=None):
        if time is None:
            time = datetime.datetime.now()
        log_str = str(time) + " " + log_str
        print log_str
        self.logfile.write(log_str + "\r\n")

def main():
    parser = OptionParser()
    
    parser.add_option("-s", "--start-freq", type="float", default=None, help="Start of frequency sweep [default=%default]")
    parser.add_option("-q", "--stop-freq", type="float", default=None, help="Stop of frequency sweep [default=%default]")
    parser.add_option("-i", "--step-freq", type="float", default=10e3, help="Step of frequency sweep [default=%default]")
    parser.add_option("-t", "--interval", type="float", default=5.0, help="Time between commands. (seconds) [default=%default]")
    parser.add_option("-S", "--start-offset", type="float", default=None, help="offset start (Hz) [default=%default]")
    
    parser.add_option("-e", "--preamble-length", type="int", default=539, help="Number of leading 0s before command is transmitted [default=%default]")
    parser.add_option("-p", "--cmd-port", type="int", default=52002, help="CMD Host Port [default=%default]")
    parser.add_option("-a", "--cmd-host", type="string", default="127.0.0.1",help="CMD Host Address [default=%default]")
    parser.add_option("-x", "--xml-host", type="string", default="127.0.0.1",help="XML Host address [default=%default]")
    parser.add_option("-y", "--xml-port", type="int", default=52003,help="XML Host Port [default=%default]")
    parser.add_option('-I', "--run-inversion",action="store_true",default=False,help="Run data inversion [default=%default]")
    parser.add_option("-m", "--pm-values", type="string", default="1.0",help="Phase modulaton values to test [default=%default]")
    parser.add_option("-f", "--command-filename",type="string",default="ref_cmd.txt",help="File path with the command list [default=%default]")
    parser.add_option("-c", "--command",type="string",help="Specific commands you would like to send (comma delimited)")
    parser.add_option("-F", "--flush", type="int", default=10, help="bits of front/rear padding [default=%default]")
    parser.add_option('-C', "--clocked-flush",action="store_true",default=False,help="clocked flush (alternating 0/1) [default=%default]")
    parser.add_option('-d', "--drop-carrier",action="store_true",default=False, help="separate individual commands in a sequence [default=%default]")
    parser.add_option('-l', "--loop",action="store_true",default=False, help="loop sending [default=%default]")
    parser.add_option("-T", "--stitch-delay", type="int", default=DATARATE, help="# of bits between coalesced commands [default=%default]")
    parser.add_option("-D", "--rollover-delay", type="float", default=0.0, help="seconds to wait on rollover [default=%default]")
    parser.add_option('-w', "--sweep",action="store_true",default=False, help="sweep back and forth [default=%default]")
    parser.add_option('-W', "--sweep-direction", type="float", default=1.0, help="+/- 1.0 sweep direction [default=%default]")
    
    (options, args) = parser.parse_args()
    
    ctrl_client = xmlrpc_client(options.xml_host,options.xml_port)
    cmd_client = socket_cmd(options.cmd_host,options.cmd_port)
    
    time_format = "%Y_%m_%d-%H_%M_%S"
    
    time_str = time.strftime(time_format)
    
    stop_freq = float(options.stop_freq)
    start_freq = float(options.start_freq)
    step_freq = float(options.step_freq)
    interval = float(options.interval)
    preamble_length = int(options.preamble_length)
    
    cmd_dict = {}
    cmds = []
    
    #get contents of command file
    try:
        cmd_file = open(options.command_filename, "r")
        cmd_content = cmd_file.readlines()
        
        for line in cmd_content:
            line = line.strip()
            
            #parts = line.strip().split("#")[0]
            
            idx = line.find('#')
            if idx > -1:
                parts = line[:idx]
            else:
                parts = line
            
            parts = parts.split()
            
            if len(parts) == 2:
                if parts[0] in cmd_dict.keys():
                    print "Warning: command %s occurs in command file %s more than once!" % (parts[0],options.command_filename)
                    sys.exit(0)
                
                if len(parts[1]) != 60:
                    print "Warning: command %s in command file %s does not have 60 bits.  Had %d" % (parts[0],options.command_filename,len(parts[1]))
                    sys.exit(0)
                
                cmd_dict[parts[0]] = parts[1]
                
                print "Added command %s (%d bits)" % (parts[0], len(parts[1]))
        
        flush = [0]*options.flush
        if options.clocked_flush:
            flush = [0,1]*(options.flush/2)
        
        commands = options.command.split(',')
        for command in commands:
            if command in cmd_dict.keys():
                cmd = cmd_dict[command]
                cmd = map(int, list(cmd))
                #for i in range(len(cmd)):
                #    cmd[i] = int(cmd[i])
                if options.drop_carrier:
                    uplink_frame = flush + ([0] * preamble_length) + [1] + cmd + flush
                    print "Uplink '%s' frame length: %d (preamble length: %d, command length: %d, flush length: %d)" % (command, len(uplink_frame), preamble_length, len(cmd), len(flush))
                    frame_tx_duration = 1.0 * len(uplink_frame) / DATARATE
                    if frame_tx_duration > interval:
                        print "Interval %f sec not long enough for frame transmission (%f sec)" % (interval, frame_tx_duration)
                        sys.exit(0)
                    cmds += [(command, uplink_frame)]
                else:
                    uplink_frame = ([0] * options.stitch_delay) + [1] + cmd
                    print "Uplink '%s' frame length: %d (stitch delay: %d, command length: %d)" % (command, len(uplink_frame), options.stitch_delay, len(cmd))
                    if len(cmds) == 0:
                        cmds = [(command,uplink_frame)]
                    else:
                        existing_command, existing_uplink_frame = cmds[0]
                        cmds = [(existing_command + "," + command, existing_uplink_frame + uplink_frame)]
            else:
                logger.log("Could not find command '%s' in file %s" % (options.command,options.command_filename))
                sys.exit(0)
        
        if not options.drop_carrier:
            (existing_command, existing_uplink_frame) = cmds[0]
            existing_uplink_frame = flush + ([0] * preamble_length) + existing_uplink_frame + flush
            cmds = [(existing_command, existing_uplink_frame)]
            frame_tx_duration = 1.0 * len(existing_uplink_frame) / DATARATE
            logger.log("Total command duration: %f sec" % (frame_tx_duration))
            if frame_tx_duration > interval:
                print "Changing interval to frame duration"
                interval = frame_tx_duration
    
    except Exception, ex:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    if options.start_freq is not None or options.stop_freq is not None:
        if not (options.start_freq is not None and options.stop_freq is not None) and ( options.start_freq < options.stop_freq ):
            print "Must specify both start and stop frequency, not just one.  Start freq must be less than stop freq"
            sys.exit(0)
    
    logger = log_this("uplink-" + time_str + ".log")
    
    if options.run_inversion:
        print "Running inversion"
        run_invert = -1
        inv_mult = 2                             #used to calc num of points
    else:
        print "Not running inversion"
        run_invert = 1
        inv_mult = 1
    
    #Get pm values
    pm_index = 0    
    pm_values = options.pm_values
    pm_values = pm_values.split(",")
    pm_values = map(float,pm_values)
    pm_value_size = len(pm_values)
    
    #count all bits - preamble, sync bit, cmd length, start and end pad (10 bits), determine if they fit in specified interval
    #if ( ( preamble_length + 1 + CMDLEN + 10 + 10)/ DATARATE > interval):
    #    print "WARNING WARNING WARNING: Interval %f too short for uplink packet with %d bits (including preamble)." % (interval,preamble_length + 1 + 60 + 20) 
    #    time.sleep(5) 
    
    #Calculate number of points and time
    points = (math.floor((stop_freq - start_freq)/step_freq)+1) * inv_mult * pm_value_size
    time_to_finish = points * interval * len(cmds)
    logger.log( "Test has %d points.  Will take %f minutes to complete." % (points,time_to_finish/60.0))
    
    #Log the paramters of this run
    logger.log("Start Time: %s" % time.strftime("%d/%m/%y %H:%M:%S"))
    logger.log("Command Names: %s" % options.command)
    #logger.log("Using command: " + str(cmd))
    logger.log("Interval: %f" % interval)
    logger.log("Preamble Lenght: %d" % preamble_length)
    logger.log("Start Freq: %.2f, Stop Freq: %.2f, Step Freq: %.2f, Start Offset: %.2f" % (start_freq, stop_freq, step_freq, options.start_offset))
    logger.log("XML Port: %d XML Host %s" % (int(options.xml_port),options.xml_host))
    logger.log("CMD Port: %d CMD Host %s" % (int(options.cmd_port),options.cmd_host))
    logger.log("Pulling commands from: %s" % options.command_filename)
    
    #initialize some things before we start the loop
    current_freq = start_freq
    if options.start_offset is not None:
        current_freq = options.start_offset
    start_time = time.time()
    invert = 1
    sweep_direction = options.sweep_direction
    
    try:
        while True:
            ctrl_client.set_freq(current_freq)
            ctrl_client.set_pm(pm_values[pm_index])
            ctrl_client.set_invert(invert)
            
            time.sleep(0.005)
            
            for (name,cmd) in cmds:
                cmd_client.send_cmd(cmd)
                logger.log("Sent cmd '%s' at %.2f Hz with polarity %d, PM of %f at %s." % (name, current_freq, invert, pm_values[pm_index], time.strftime("%d/%m/%y %H:%M:%S")))
                logger.log(str(cmd))
                time.sleep(interval)
            
            if (pm_index == (pm_value_size-1)):
                if (invert==1):
                    #current_freq += step_freq
                    current_freq += (sweep_direction * step_freq)
                    if ((sweep_direction > 0) and (current_freq > stop_freq)) or ((sweep_direction < 0) and (current_freq < start_freq)):
                        print "Frequency rollover (direction: %f)." % (sweep_direction)
                        if not options.loop:
                            break
                        time.sleep(options.rollover_delay)
                        if options.sweep:
                            sweep_direction *= -1.0
                            #current_freq += (sweep_direction * step_freq)
                            if sweep_direction < 0.0:
                                current_freq = stop_freq
                            else:
                                current_freq = start_freq
                        else:
                            current_freq = start_freq
                invert *= run_invert
            
            pm_index = ( pm_index + 1 ) % pm_value_size
    except KeyboardInterrupt:
        pass
    except Exception, ex:
        print "Unhandled exception:", ex
    
    ctrl_client.set_freq(0)

if __name__ == '__main__':
    main()
