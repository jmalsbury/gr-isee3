#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Uplink
# Generated: Wed May 21 22:04:01 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import SimpleXMLRPCServer
import isee3
import threading
import time
import wx

class uplink(grc_wxgui.top_block_gui):

    def __init__(self, sym_rate=256, samp_per_sym=256, rx_gain=15, tx_gain=15, nominal_uplink_freq=2041.95e6, lo_off=5e6, backoff=0.150):
        grc_wxgui.top_block_gui.__init__(self, title="Uplink")

        ##################################################
        # Parameters
        ##################################################
        self.sym_rate = sym_rate
        self.samp_per_sym = samp_per_sym
        self.rx_gain = rx_gain
        self.tx_gain = tx_gain
        self.nominal_uplink_freq = nominal_uplink_freq
        self.lo_off = lo_off
        self.backoff = backoff

        ##################################################
        # Variables
        ##################################################
        self.f1 = f1 = 9000.0
        self.f0 = f0 = 7500.0
        self.deviation = deviation = (f0- f1)/2.0
        self.variable_0 = variable_0 = 0
        self.subcarrier_freq = subcarrier_freq = f1+deviation
        self.samp_rate = samp_rate = 250000
        self.pre_resamp_rate = pre_resamp_rate = sym_rate*samp_per_sym
        self.pm = pm = 1.2
        self.invert = invert = 1
        self.doppler = doppler = 0

        ##################################################
        # Blocks
        ##################################################
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Output FFT")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Input FFT")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Input Phase/Mag")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Mod Clk/Data")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "PM Output Scope")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "PM Input")
        self.Add(self.nb)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(("", 52003), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        threading.Thread(target=self.xmlrpc_server_0.serve_forever).start()
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
        	self.nb.GetPage(5).GetWin(),
        	title="Scope Plot",
        	sample_rate=pre_resamp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(5).Add(self.wxgui_scopesink2_2.win)
        self.wxgui_scopesink2_1 = scopesink2.scope_sink_c(
        	self.nb.GetPage(4).GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(4).Add(self.wxgui_scopesink2_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.nb.GetPage(2).GetWin(),
        	title="Scope Plot",
        	sample_rate=pre_resamp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(2).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0_1 = fftsink2.fft_sink_c(
        	self.nb.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=256,
        	fft_rate=10,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.nb.GetPage(1).Add(self.wxgui_fftsink2_0_1.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.nb.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=256,
        	fft_rate=10,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.nb.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	"",
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(nominal_uplink_freq,lo_off), 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	"",
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(nominal_uplink_freq,lo_off), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.pfb_arb_resampler_xxx_0_0 = pfb.arb_resampler_ccc(
        	  float(pre_resamp_rate)/float(samp_rate),
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0_0.declare_sample_delay(0)
        	
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  float(samp_rate)/float(pre_resamp_rate),
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.clock_and_data = scopesink2.scope_sink_c(
        	self.nb.GetPage(3).GetWin(),
        	title="Scope Plot",
        	sample_rate=pre_resamp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(3).Add(self.clock_and_data.win)
        self.carrier = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, doppler, 1*backoff, 0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f(tuple([1] * (samp_per_sym/4) +  [0] * (samp_per_sym/4) +  [0] * (samp_per_sym/4) +  [1] * (samp_per_sym/4)), True, 1, [])
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", "52002", 10000, False)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, samp_per_sym)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff((4000, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((0.666, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((invert, ))
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_float_to_complex_2 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_vff((0.333, ))
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((-1, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0, ))
        self.binary_to_pdu0 = isee3.binary_to_pdu()
        self.analog_sig_source_x_0 = analog.sig_source_c(pre_resamp_rate, analog.GR_COS_WAVE, subcarrier_freq, 1/1.333, 0)
        self.analog_phase_modulator_fc_1 = analog.phase_modulator_fc(pm/2.0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(float(deviation)/float(pre_resamp_rate)*3.1415*2.0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_add_const_vxx_1_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_float_to_complex_2, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_float_to_complex_2, 1))
        self.connect((self.blocks_float_to_complex_2, 0), (self.blocks_multiply_xx_0, 2))
        self.connect((self.blocks_float_to_complex_1, 0), (self.clock_and_data, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.carrier, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_float_to_complex_1, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_float_to_complex_1_0, 1))
        self.connect((self.blocks_float_to_complex_1_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0_1, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_float_to_complex_1_0, 0))
        self.connect((self.analog_phase_modulator_fc_1, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.analog_phase_modulator_fc_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.wxgui_scopesink2_2, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.binary_to_pdu0, "pdu_out", self.blocks_pdu_to_tagged_stream_0, "pdus")
        self.msg_connect(self.blocks_socket_pdu_0, "pdus", self.binary_to_pdu0, "binary_in")
        self.msg_connect(self.binary_to_pdu0, "pdu_out", self.blocks_message_debug_0, "print_pdu")

# QT sink close method reimplementation

    def get_sym_rate(self):
        return self.sym_rate

    def set_sym_rate(self, sym_rate):
        self.sym_rate = sym_rate
        self.set_pre_resamp_rate(self.sym_rate*self.samp_per_sym)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_pre_resamp_rate(self.sym_rate*self.samp_per_sym)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_nominal_uplink_freq(self):
        return self.nominal_uplink_freq

    def set_nominal_uplink_freq(self, nominal_uplink_freq):
        self.nominal_uplink_freq = nominal_uplink_freq
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq,self.lo_off), 0)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq,self.lo_off), 0)

    def get_lo_off(self):
        return self.lo_off

    def set_lo_off(self, lo_off):
        self.lo_off = lo_off
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq,self.lo_off), 0)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq,self.lo_off), 0)

    def get_backoff(self):
        return self.backoff

    def set_backoff(self, backoff):
        self.backoff = backoff
        self.carrier.set_amplitude(1*self.backoff)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.set_subcarrier_freq(self.f1+self.deviation)
        self.set_deviation((self.f0- self.f1)/2.0)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.set_deviation((self.f0- self.f1)/2.0)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_subcarrier_freq(self.f1+self.deviation)
        self.analog_frequency_modulator_fc_0.set_sensitivity(float(self.deviation)/float(self.pre_resamp_rate)*3.1415*2.0)

    def get_variable_0(self):
        return self.variable_0

    def set_variable_0(self, variable_0):
        self.variable_0 = variable_0

    def get_subcarrier_freq(self):
        return self.subcarrier_freq

    def set_subcarrier_freq(self, subcarrier_freq):
        self.subcarrier_freq = subcarrier_freq
        self.analog_sig_source_x_0.set_frequency(self.subcarrier_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.wxgui_fftsink2_0_1.set_sample_rate(self.samp_rate)
        self.pfb_arb_resampler_xxx_0_0.set_rate(float(self.pre_resamp_rate)/float(self.samp_rate))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate)
        self.carrier.set_sampling_freq(self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(float(self.samp_rate)/float(self.pre_resamp_rate))

    def get_pre_resamp_rate(self):
        return self.pre_resamp_rate

    def set_pre_resamp_rate(self, pre_resamp_rate):
        self.pre_resamp_rate = pre_resamp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity(float(self.deviation)/float(self.pre_resamp_rate)*3.1415*2.0)
        self.wxgui_scopesink2_0.set_sample_rate(self.pre_resamp_rate)
        self.pfb_arb_resampler_xxx_0_0.set_rate(float(self.pre_resamp_rate)/float(self.samp_rate))
        self.clock_and_data.set_sample_rate(self.pre_resamp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(float(self.samp_rate)/float(self.pre_resamp_rate))
        self.wxgui_scopesink2_2.set_sample_rate(self.pre_resamp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.pre_resamp_rate)

    def get_pm(self):
        return self.pm

    def set_pm(self, pm):
        self.pm = pm
        self.analog_phase_modulator_fc_1.set_sensitivity(self.pm/2.0)

    def get_invert(self):
        return self.invert

    def set_invert(self, invert):
        self.invert = invert
        self.blocks_multiply_const_vxx_0.set_k((self.invert, ))

    def get_doppler(self):
        return self.doppler

    def set_doppler(self, doppler):
        self.doppler = doppler
        self.carrier.set_frequency(self.doppler)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--sym-rate", dest="sym_rate", type="eng_float", default=eng_notation.num_to_str(256),
        help="Set sym_rate [default=%default]")
    parser.add_option("", "--samp-per-sym", dest="samp_per_sym", type="intx", default=256,
        help="Set samp_per_sym [default=%default]")
    parser.add_option("", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(15),
        help="Set rx_gain [default=%default]")
    parser.add_option("", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(15),
        help="Set tx_gain [default=%default]")
    parser.add_option("", "--nominal-uplink-freq", dest="nominal_uplink_freq", type="eng_float", default=eng_notation.num_to_str(2041.95e6),
        help="Set nominal_uplink_freq [default=%default]")
    parser.add_option("", "--lo-off", dest="lo_off", type="eng_float", default=eng_notation.num_to_str(5e6),
        help="Set lo_off [default=%default]")
    parser.add_option("", "--backoff", dest="backoff", type="eng_float", default=eng_notation.num_to_str(0.150),
        help="Set backoff [default=%default]")
    (options, args) = parser.parse_args()
    tb = uplink(sym_rate=options.sym_rate, samp_per_sym=options.samp_per_sym, rx_gain=options.rx_gain, tx_gain=options.tx_gain, nominal_uplink_freq=options.nominal_uplink_freq, lo_off=options.lo_off, backoff=options.backoff)
    tb.Start(True)
    tb.Wait()

