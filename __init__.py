from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import (
    MIDI_NOTE_TYPE,
)

CHANNEL = 0


class Button(ButtonElement):
    momentary = True
    msg_type = MIDI_NOTE_TYPE
    channel = CHANNEL

    def __init__(self, note):
        ButtonElement.__init__(
            self,
            self.momentary,
            self.msg_type,
            self.channel,
            note)


class Transport(ControlSurface):

    def __init__(self, c):
        ControlSurface.__init__(self, c)

        # Turn off rebuild MIDI map until after we're done setting up.
        self.set_suppress_rebuild_requests(True)
        self.transport()
        self.set_suppress_rebuild_requests(False)

    def transport(self):
        transport = TransportComponent()
        transport.set_play_button(Button(61))


def create_instance(c):
    return Transport(c)
