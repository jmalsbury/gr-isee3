#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Uplink
# Generated: Wed Jun 18 16:22:49 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import SimpleXMLRPCServer
import isee3
import mac
import math
import pmt
import threading
import time
import time, os
import wx

class uplink(grc_wxgui.top_block_gui):

    def __init__(self, sym_rate=256, samp_per_sym=256, nominal_uplink_freq=2041.95e6*0 + 2041.9479e6 + 1e6*0, lo_off=5e6 * 0, tx_gain=15*0 + 13.5*0, backoff=0.150*0 + (0.6+0.1)*0 + 1e-3, record_path='/media/balint/PATRIOT/ICE/TX/'):
        grc_wxgui.top_block_gui.__init__(self, title="Uplink")

        ##################################################
        # Parameters
        ##################################################
        self.sym_rate = sym_rate
        self.samp_per_sym = samp_per_sym
        self.nominal_uplink_freq = nominal_uplink_freq
        self.lo_off = lo_off
        self.tx_gain = tx_gain
        self.backoff = backoff
        self.record_path = record_path

        ##################################################
        # Variables
        ##################################################
        self.time_format = time_format = "%Y-%d-%m_%H-%M-%S"
        self.time_now = time_now = time.strftime(time_format)
        self.samp_rate = samp_rate = 250000
        self.pre_resamp_rate = pre_resamp_rate = sym_rate * samp_per_sym
        self.f1 = f1 = 9000.0
        self.f0 = f0 = 7500.0
        self.resamp_rate = resamp_rate = float(samp_rate)/float(pre_resamp_rate)
        self.pm = pm = 1.2*0 + 1.0
        self.nominal_uplink_freq_chooser = nominal_uplink_freq_chooser = nominal_uplink_freq
        self.manual_doppler = manual_doppler = 0
        self.file_name = file_name = time_now + ".mcfile"
        self.doppler = doppler = 0
        self.deviation = deviation = (f1 - f0) / 2.0
        self.tx_gain_user = tx_gain_user = tx_gain
        self.subcarrier_freq = subcarrier_freq = f0 + deviation
        self.source = source = ''
        self.pm_txt = pm_txt = pm
        self.nominal_uplink_freq_user = nominal_uplink_freq_user = nominal_uplink_freq_chooser
        self.lo_off_user = lo_off_user = lo_off
        self.length_mul = length_mul = float(samp_per_sym) * resamp_rate
        self.invert = invert = 1
        self.final_record_path = final_record_path = os.path.join(record_path, file_name)
        self.final_doppler = final_doppler = doppler + manual_doppler
        self.backoff_user = backoff_user = backoff

        ##################################################
        # Blocks
        ##################################################
        _tx_gain_user_sizer = wx.BoxSizer(wx.VERTICAL)
        self._tx_gain_user_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_tx_gain_user_sizer,
        	value=self.tx_gain_user,
        	callback=self.set_tx_gain_user,
        	label="TX Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._tx_gain_user_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_tx_gain_user_sizer,
        	value=self.tx_gain_user,
        	callback=self.set_tx_gain_user,
        	minimum=0,
        	maximum=32,
        	num_steps=32,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_tx_gain_user_sizer)
        self._nominal_uplink_freq_user_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.nominal_uplink_freq_user,
        	callback=self.set_nominal_uplink_freq_user,
        	label="Nominal Uplink Freq",
        	converter=forms.float_converter(),
        )
        self.Add(self._nominal_uplink_freq_user_text_box)
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Output FFT")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Input FFT")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Input Phase/Mag")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Mod Clk/Data")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "PM Output Scope")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "PM Input")
        self.Add(self.nb)
        self._lo_off_user_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.lo_off_user,
        	callback=self.set_lo_off_user,
        	label="LO Offset",
        	converter=forms.float_converter(),
        )
        self.Add(self._lo_off_user_text_box)
        self._final_doppler_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.final_doppler,
        	callback=self.set_final_doppler,
        	label="Final Doppler",
        	converter=forms.float_converter(),
        )
        self.Add(self._final_doppler_static_text)
        self._doppler_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.doppler,
        	callback=self.set_doppler,
        	label="Doppler Shift",
        	converter=forms.float_converter(),
        )
        self.Add(self._doppler_text_box)
        _backoff_user_sizer = wx.BoxSizer(wx.VERTICAL)
        self._backoff_user_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_backoff_user_sizer,
        	value=self.backoff_user,
        	callback=self.set_backoff_user,
        	label="Backoff",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._backoff_user_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_backoff_user_sizer,
        	value=self.backoff_user,
        	callback=self.set_backoff_user,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_backoff_user_sizer)
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
        	peak_hold=False,	fft_in=False,
        	always_run=False,
        	fft_out=False,
        )
        self.nb.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"",
        	True,
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(nominal_uplink_freq_user,lo_off_user), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain*0 + tx_gain_user, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate),
                decimation=int(pre_resamp_rate),
                taps=None,
                fractional_bw=None,
        )
        self._pm_txt_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.pm_txt,
        	callback=self.set_pm_txt,
        	label="Phase Moduation Index",
        	converter=forms.float_converter(),
        )
        self.Add(self._pm_txt_static_text)
        self._nominal_uplink_freq_chooser_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.nominal_uplink_freq_chooser,
        	callback=self.set_nominal_uplink_freq_chooser,
        	label="Nomial Uplink Frequency",
        	choices=[2041.9479e6, 2090.66e6],
        	labels=['B: 2041.9479', 'A: 2090.66'],
        )
        self.Add(self._nominal_uplink_freq_chooser_chooser)
        self._manual_doppler_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.manual_doppler,
        	callback=self.set_manual_doppler,
        	label="Manual Doppler",
        	converter=forms.float_converter(),
        )
        self.Add(self._manual_doppler_text_box)
        self.mac_burst_tagger_0 = mac.burst_tagger('packet_len', length_mul, 256, 32*0 + 256, True, False)
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
        self.carrier = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, doppler*0 + final_doppler, 0*backoff + backoff_user, 0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f(tuple([1] * (samp_per_sym/4) +  [0] * (samp_per_sym/4) +  [0] * (samp_per_sym/4) +  [1] * (samp_per_sym/4)), True, 1, [])
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", "52002", 10000, False)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, samp_per_sym)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len", 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((2.0/3, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((invert, ))
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.cons(pmt.to_pmt({'ignore': True}), pmt.init_u8vector(1, 1*[0])), 0)
        self.blocks_float_to_complex_2 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, final_record_path, samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", True)
        self.blocks_file_meta_sink_0.set_unbuffered(False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_vff((1.0/3, ))
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((-1, ))
        self.binary_to_pdu0 = isee3.binary_to_pdu()
        self.analog_sig_source_x_0 = analog.sig_source_c(pre_resamp_rate, analog.GR_COS_WAVE, subcarrier_freq, 1/1.333, 0)
        self.analog_phase_modulator_fc_1 = analog.phase_modulator_fc(pm / (2.0*0 + 1))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(float(deviation) / float(pre_resamp_rate) * math.pi*2.0)

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
        self.connect((self.blocks_float_to_complex_1, 0), (self.clock_and_data, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.carrier, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_float_to_complex_1, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.analog_phase_modulator_fc_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.wxgui_scopesink2_2, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_float_to_complex_2, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.blocks_float_to_complex_2, 0), (self.blocks_multiply_xx_0, 2))
        self.connect((self.mac_burst_tagger_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.mac_burst_tagger_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.analog_phase_modulator_fc_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.mac_burst_tagger_0, 0), (self.blocks_file_meta_sink_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.binary_to_pdu0, "pdu_out", self.blocks_pdu_to_tagged_stream_0, "pdus")
        self.msg_connect(self.blocks_socket_pdu_0, "pdus", self.binary_to_pdu0, "binary_in")
        self.msg_connect(self.blocks_message_strobe_0_0, "strobe", self.blocks_pdu_to_tagged_stream_0, "pdus")
        self.msg_connect(self.uhd_usrp_sink_0, "ctl", self.blocks_message_strobe_0_0, "trigger")

# QT sink close method reimplementation

    def get_sym_rate(self):
        return self.sym_rate

    def set_sym_rate(self, sym_rate):
        self.sym_rate = sym_rate
        self.set_pre_resamp_rate(self.sym_rate * self.samp_per_sym)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_pre_resamp_rate(self.sym_rate * self.samp_per_sym)
        self.set_length_mul(float(self.samp_per_sym) * self.resamp_rate)

    def get_nominal_uplink_freq(self):
        return self.nominal_uplink_freq

    def set_nominal_uplink_freq(self, nominal_uplink_freq):
        self.nominal_uplink_freq = nominal_uplink_freq
        self.set_nominal_uplink_freq_chooser(self.nominal_uplink_freq)

    def get_lo_off(self):
        return self.lo_off

    def set_lo_off(self, lo_off):
        self.lo_off = lo_off
        self.set_lo_off_user(self.lo_off)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.set_tx_gain_user(self.tx_gain)
        self.uhd_usrp_sink_0.set_gain(self.tx_gain*0 + self.tx_gain_user, 0)

    def get_backoff(self):
        return self.backoff

    def set_backoff(self, backoff):
        self.backoff = backoff
        self.set_backoff_user(self.backoff)
        self.carrier.set_amplitude(0*self.backoff + self.backoff_user)

    def get_record_path(self):
        return self.record_path

    def set_record_path(self, record_path):
        self.record_path = record_path
        self.set_final_record_path(os.path.join(self.record_path, self.file_name))

    def get_time_format(self):
        return self.time_format

    def set_time_format(self, time_format):
        self.time_format = time_format
        self.set_time_now(time.strftime(self.time_format))

    def get_time_now(self):
        return self.time_now

    def set_time_now(self, time_now):
        self.time_now = time_now
        self.set_file_name(self.time_now + ".mcfile")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_resamp_rate(float(self.samp_rate)/float(self.pre_resamp_rate))
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.carrier.set_sampling_freq(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_pre_resamp_rate(self):
        return self.pre_resamp_rate

    def set_pre_resamp_rate(self, pre_resamp_rate):
        self.pre_resamp_rate = pre_resamp_rate
        self.set_resamp_rate(float(self.samp_rate)/float(self.pre_resamp_rate))
        self.clock_and_data.set_sample_rate(self.pre_resamp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.pre_resamp_rate)
        self.wxgui_scopesink2_2.set_sample_rate(self.pre_resamp_rate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(float(self.deviation) / float(self.pre_resamp_rate) * math.pi*2.0)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.set_deviation((self.f1 - self.f0) / 2.0)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.set_subcarrier_freq(self.f0 + self.deviation)
        self.set_deviation((self.f1 - self.f0) / 2.0)

    def get_resamp_rate(self):
        return self.resamp_rate

    def set_resamp_rate(self, resamp_rate):
        self.resamp_rate = resamp_rate
        self.set_length_mul(float(self.samp_per_sym) * self.resamp_rate)

    def get_pm(self):
        return self.pm

    def set_pm(self, pm):
        self.pm = pm
        self.analog_phase_modulator_fc_1.set_sensitivity(self.pm / (2.0*0 + 1))
        self.set_pm_txt(self.pm)

    def get_nominal_uplink_freq_chooser(self):
        return self.nominal_uplink_freq_chooser

    def set_nominal_uplink_freq_chooser(self, nominal_uplink_freq_chooser):
        self.nominal_uplink_freq_chooser = nominal_uplink_freq_chooser
        self.set_nominal_uplink_freq_user(self.nominal_uplink_freq_chooser)
        self._nominal_uplink_freq_chooser_chooser.set_value(self.nominal_uplink_freq_chooser)

    def get_manual_doppler(self):
        return self.manual_doppler

    def set_manual_doppler(self, manual_doppler):
        self.manual_doppler = manual_doppler
        self._manual_doppler_text_box.set_value(self.manual_doppler)
        self.set_final_doppler(self.doppler + self.manual_doppler)

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.set_final_record_path(os.path.join(self.record_path, self.file_name))

    def get_doppler(self):
        return self.doppler

    def set_doppler(self, doppler):
        self.doppler = doppler
        self._doppler_text_box.set_value(self.doppler)
        self.carrier.set_frequency(self.doppler*0 + self.final_doppler)
        self.set_final_doppler(self.doppler + self.manual_doppler)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_subcarrier_freq(self.f0 + self.deviation)
        self.analog_frequency_modulator_fc_0.set_sensitivity(float(self.deviation) / float(self.pre_resamp_rate) * math.pi*2.0)

    def get_tx_gain_user(self):
        return self.tx_gain_user

    def set_tx_gain_user(self, tx_gain_user):
        self.tx_gain_user = tx_gain_user
        self._tx_gain_user_slider.set_value(self.tx_gain_user)
        self._tx_gain_user_text_box.set_value(self.tx_gain_user)
        self.uhd_usrp_sink_0.set_gain(self.tx_gain*0 + self.tx_gain_user, 0)

    def get_subcarrier_freq(self):
        return self.subcarrier_freq

    def set_subcarrier_freq(self, subcarrier_freq):
        self.subcarrier_freq = subcarrier_freq
        self.analog_sig_source_x_0.set_frequency(self.subcarrier_freq)

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source

    def get_pm_txt(self):
        return self.pm_txt

    def set_pm_txt(self, pm_txt):
        self.pm_txt = pm_txt
        self._pm_txt_static_text.set_value(self.pm_txt)

    def get_nominal_uplink_freq_user(self):
        return self.nominal_uplink_freq_user

    def set_nominal_uplink_freq_user(self, nominal_uplink_freq_user):
        self.nominal_uplink_freq_user = nominal_uplink_freq_user
        self._nominal_uplink_freq_user_text_box.set_value(self.nominal_uplink_freq_user)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq_user,self.lo_off_user), 0)

    def get_lo_off_user(self):
        return self.lo_off_user

    def set_lo_off_user(self, lo_off_user):
        self.lo_off_user = lo_off_user
        self._lo_off_user_text_box.set_value(self.lo_off_user)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.nominal_uplink_freq_user,self.lo_off_user), 0)

    def get_length_mul(self):
        return self.length_mul

    def set_length_mul(self, length_mul):
        self.length_mul = length_mul

    def get_invert(self):
        return self.invert

    def set_invert(self, invert):
        self.invert = invert
        self.blocks_multiply_const_vxx_0.set_k((self.invert, ))

    def get_final_record_path(self):
        return self.final_record_path

    def set_final_record_path(self, final_record_path):
        self.final_record_path = final_record_path
        self.blocks_file_meta_sink_0.open(self.final_record_path)

    def get_final_doppler(self):
        return self.final_doppler

    def set_final_doppler(self, final_doppler):
        self.final_doppler = final_doppler
        self.carrier.set_frequency(self.doppler*0 + self.final_doppler)
        self._final_doppler_static_text.set_value(self.final_doppler)

    def get_backoff_user(self):
        return self.backoff_user

    def set_backoff_user(self, backoff_user):
        self.backoff_user = backoff_user
        self._backoff_user_slider.set_value(self.backoff_user)
        self._backoff_user_text_box.set_value(self.backoff_user)
        self.carrier.set_amplitude(0*self.backoff + self.backoff_user)

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
    parser.add_option("", "--nominal-uplink-freq", dest="nominal_uplink_freq", type="eng_float", default=eng_notation.num_to_str(2041.95e6*0 + 2041.9479e6 + 1e6*0),
        help="Set nominal_uplink_freq [default=%default]")
    parser.add_option("", "--lo-off", dest="lo_off", type="eng_float", default=eng_notation.num_to_str(5e6 * 0),
        help="Set LO Offset [default=%default]")
    parser.add_option("", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(15*0 + 13.5*0),
        help="Set TX Gain [default=%default]")
    parser.add_option("", "--backoff", dest="backoff", type="eng_float", default=eng_notation.num_to_str(0.150*0 + (0.6+0.1)*0 + 1e-3),
        help="Set backoff [default=%default]")
    parser.add_option("", "--record-path", dest="record_path", type="string", default='/media/balint/PATRIOT/ICE/TX/',
        help="Set path to record baseband [default=%default]")
    (options, args) = parser.parse_args()
    tb = uplink(sym_rate=options.sym_rate, samp_per_sym=options.samp_per_sym, nominal_uplink_freq=options.nominal_uplink_freq, lo_off=options.lo_off, tx_gain=options.tx_gain, backoff=options.backoff, record_path=options.record_path)
    tb.Start(True)
    tb.Wait()
