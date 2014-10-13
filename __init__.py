from __future__ import with_statement

import Live
from _Framework.ButtonElement import ButtonElement
# from _Framework.ButtonMatrixElement import ButtonMatrixElement
# from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.EncoderElement import EncoderElement
# from _Framework.Layer import Layer
# from _Framework.MixerComponent import MixerComponent
# from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
# from _Framework.TransportComponent import TransportComponent

from _Generic.SpecialMixerComponent import SpecialMixerComponent

from _Framework.InputControlElement import (
    MIDI_CC_TYPE,
    MIDI_NOTE_TYPE,
)

CHANNEL = 14
TRACKS = 4
SCENES = 4
MAP_MODE = Live.MidiMap.MapMode


class Fader(SliderElement):
    channel = CHANNEL

    def __init__(self, identifier):
        SliderElement.__init__(
            self,
            MIDI_CC_TYPE,
            self.channel,
            identifier)


class Note(ButtonElement):
    channel = CHANNEL

    def __init__(self, identifier):
        ButtonElement.__init__(
            self,
            momentary=True,
            msg_type=MIDI_NOTE_TYPE,
            channel=self.channel,
            identifier=identifier)


class Encoder(EncoderElement):
    channel = CHANNEL
    map_mode = MAP_MODE.absolute

    def __init__(self, identifier):
        EncoderElement.__init__(
            self,
            msg_type=MIDI_CC_TYPE,
            channel=self.channel,
            identifier=identifier,
            map_mode=self.map_mode)


class Mixer(SpecialMixerComponent):
    tracks = TRACKS

    def __init__(self):
        SpecialMixerComponent.__init__(
            self,
            self.tracks)
        self.name = 'Mixer'
        self.strips()

    def strips(self):
        for track in range(self.tracks):
            self.strip(track)

    def strip(self, track):
        strip = self.channel_strip(track)
        strip.name = "Channel_Strip_%d" % track
        fader = VolumeFader(track)
        strip.set_volume_control(fader)
        return strip


class VolumeFader(Encoder):
    ccs = [16, 17, 18, 19]

    def __init__(self, index):
        Encoder.__init__(
            self,
            self.ccs[index])
        self.name = "Volume_Fader_%d" % index


class Controller(OptimizedControlSurface):

    def __init__(self, c):
        OptimizedControlSurface.__init__(self, c)
        with self.component_guard():
            mixer = Mixer()
            # session = self.session()
            # session.set_mixer(mixer)

    def handle_sysex(self, midi_bytes):
        pass


def create_instance(c):
    return Controller(c)
