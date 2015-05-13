from ArtNet3 import ArtNet3
from loop import Loop
from pygame_midi_input import MidiInput

import logging
log = logging.getLogger(__name__)

VERSION = '0.01'


class LightingAutomation(Loop):

    def __init__(self, framerate=30):
        super().__init__(framerate)
        self.artnet = ArtNet3()
        self.midi_input = MidiInput('nanoKONTROL2')
        self.midi_input.init_pygame()
        self.midi_input.midi_event = self.midi_event  # Dynamic POWER!!!! Remap the midi event to be on this object!

        self.loop()

    def close(self):
        self.midi_input.close()

    def render(self, frame):
        self.midi_input.process_events()

    def midi_event(self, event, data1, data2, data3):
        if data1 == 46:
            self.running = False
        print('lights2 {0} {1} {2} {3}'.format(event, data1, data2, data3))


def get_args():
    import argparse

    parser = argparse.ArgumentParser(
        prog=__name__,
        description="""Lighting Automation

        """,
        epilog="""
        """
    )
    parser_input = parser

    parser.add_argument('--log_level', type=int,  help='log level', default=logging.INFO)
    parser.add_argument('--version', action='version', version=VERSION)

    args = parser.parse_args()

    return vars(args)


if __name__ == "__main__":
    args = get_args()
    logging.basicConfig(level=args['log_level'])

    LightingAutomation()
