#!/usr/bin/env python
# 
# Copyright 2013 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
import numpy
from math import pi
from gnuradio import gr, blocks
import pmt
from gnuradio import digital
import sys
import time
import isee3
import array

GET_FEND = 0 
GET_LEN = 1
GET_PAYLOAD = 2

SELF_ADDR = 10

FEND = 0x55

class binary_to_pdu(gr.basic_block):
    """
    docstring for block pdu_link
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="binary_tp_pdu",
            in_sig=None,
            out_sig=None)

        self.message_port_register_out(pmt.intern('pdu_out'))
        self.message_port_register_in(pmt.intern('pdu_in'))
        self.set_msg_handler(pmt.intern('pdu_in'),self.handle_pdu)

        self.message_port_register_out(pmt.intern('binary_out'))
        self.message_port_register_in(pmt.intern('binary_in'))
        self.set_msg_handler(pmt.intern('binary_in'),self.handle_binary)

        self.rx_state = GET_FEND
        self.incoming_len = 0
        self.count = 0
        self.out_buf = array.array("B",( 0 for i in range(8192)))
        self.last_time = 0

    def handle_pdu(self,msg):
        #print msg
        data =  pmt.cdr(msg)
        if not pmt.is_u8vector(data):
            raise NameError("Data is not u8 vector")

        payload  = array.array("B",pmt.u8vector_elements(data))
        payload_len = len(payload)

        packet = array.array('B',(0 for i in range(0,payload_len + 5)))

        packet[0] = 0x55
        packet[1] = ( payload_len & 0xFF000000 ) >> 24
        packet[2] = ( payload_len & 0x00FF0000 ) >> 16
        packet[3] = ( payload_len & 0x0000FF00 ) >> 8
        packet[4] = ( payload_len & 0x000000FF ) >> 0
        packet[5:]= payload
        src = (packet[5] >> 1) & 0b11111
        #print src
        #print "incoming from radio",packet
        if 1:
            self.message_port_pub(pmt.intern('binary_out'),pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(len(packet),packet)))
        
    def handle_binary(self,msg):

        data =  pmt.cdr(msg)
        if not pmt.is_u8vector(data):
            raise NameError("Data is not u8 vector")
        payload  = array.array("B",pmt.u8vector_elements(data))

        buf = payload
        
        #print buf
        
        for i in buf:
            if self.rx_state == GET_FEND:
                if i == FEND:
                    self.rx_state = GET_LEN
                    self.count = 0 
                    self.incoming_len = 0
                    
            elif self.rx_state == GET_LEN:
                self.incoming_len |= ( ( i & 0xFF ) << ( 8 * (3 - self.count ) ) )
                self.count += 1
                if self.count == 4:
                    #print "PDU Link(TTY): Receiving Payload Frame of Length:",self.incoming_len,self.last_time - time.time()
                    print "<binary_to_pdu> Receiving Payload Frame of Length:", self.incoming_len
                    self.last_time = time.time()
                    if self.incoming_len < 2048:
                        self.count = 0
                        self.rx_state = GET_PAYLOAD
                    else:
                        print "Received unreasonable payload length: ",self.incoming_len, "Aborting!"
                        self.rx_state = GET_FEND
            
            elif self.rx_state == GET_PAYLOAD:
                #print self.count,len(self.out_buf),self.incoming_len
                self.out_buf[self.count] = i
                self.count += 1
                if self.count == self.incoming_len:
                    #print buf
                    self.rx_state = GET_FEND
                    packet = self.out_buf[0:self.incoming_len]
                    print "<binary_to_pdu>", packet
                    self.message_port_pub(pmt.intern('pdu_out'),pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(len(packet),packet)))
                    self.count = 0
