#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-PCAP author.
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


import numpy as np
import pmt
from scapy.all import *
from gnuradio import gr

class pdu_pcap_sink(gr.sync_block):
    """
    docstring for block pdu_pcap_sink
    """
    def __init__(self, filename, linktype):
        gr.sync_block.__init__(self,
            name="pdu_pcap_sink",
            in_sig=[],
            out_sig=[])
        self.filename = filename
        self.linktype = linktype
        self.pcap_file = scapy.utils.PcapWriter(self.filename, linktype = linktype, append = True, sync = True)
        self.message_port_register_in(pmt.intern("msg_in"))
        self.set_msg_handler(pmt.intern("msg_in"), self.handle_msg)

    def handle_msg(self, msg):
        meta = pmt.to_python(msg)
        payload = np.array([], dtype = np.uint8)
        for p in range(len(meta[1][:])):
            payload = np.append(payload, meta[1][p])
        x = payload.tobytes()
        self.pcap_file.write(x)

    def work(self, input_items, output_items):
        pass

