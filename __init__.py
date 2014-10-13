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


class Controller(OptimizedControlSurface):

    def __init__(self, c):
        OptimizedControlSurface.__init__(self, c)
        with self.component_guard():
            mixer = self.mixer()
            # session = self.session()
            # session.set_mixer(mixer)

        # Turn off rebuild MIDI map until after we're done setting up.
        # self.set_suppress_rebuild_requests(True)
        # self.transport()
        # self.set_suppress_rebuild_requests(False)

    def handle_sysex(self, midi_bytes):
        pass

    def mixer(self):
        mixer = SpecialMixerComponent(TRACKS)
        mixer.name = 'Mixer'

        mixer.master_strip().name = 'Master_Channel_Strip'
        encoder = Encoder(17)
        encoder.name = 'Master_Volume_Control'
        mixer.master_strip().set_volume_control(encoder)

        return mixer


def create_instance(c):
    return Controller(c)
