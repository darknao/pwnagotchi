import logging
from threading import RLock

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl


class WaveshareV2(DisplayImpl):
    def __init__(self, config):
        super(WaveshareV2, self).__init__(config, 'waveshare_2')
        self._display = None
        self._lock = RLock()
        self._is_full_update = None

    def layout(self):
        if self.config['color'] == 'black':
            fonts.setup(10, 9, 10, 35)
            self._layout['width'] = 250
            self._layout['height'] = 122
            self._layout['face'] = (0, 40)
            self._layout['name'] = (5, 20)
            self._layout['channel'] = (0, 0)
            self._layout['aps'] = (28, 0)
            self._layout['uptime'] = (185, 0)
            self._layout['line1'] = [0, 14, 250, 14]
            self._layout['line2'] = [0, 108, 250, 108]
            self._layout['friend_face'] = (0, 92)
            self._layout['friend_name'] = (40, 94)
            self._layout['shakes'] = (0, 109)
            self._layout['mode'] = (225, 109)
            self._layout['status'] = {
                'pos': (125, 20),
                'font': fonts.Medium,
                'max': 20
            }
        else:
            fonts.setup(10, 8, 10, 25)
            self._layout['width'] = 212
            self._layout['height'] = 104
            self._layout['face'] = (0, 26)
            self._layout['name'] = (5, 15)
            self._layout['channel'] = (0, 0)
            self._layout['aps'] = (28, 0)
            self._layout['status'] = (91, 15)
            self._layout['uptime'] = (147, 0)
            self._layout['line1'] = [0, 12, 212, 12]
            self._layout['line2'] = [0, 92, 212, 92]
            self._layout['friend_face'] = (0, 76)
            self._layout['friend_name'] = (40, 78)
            self._layout['shakes'] = (0, 93)
            self._layout['mode'] = (187, 93)
            self._layout['status'] = {
                'pos': (125, 20),
                'font': fonts.Medium,
                'max': 14
            }
        return self._layout

    def _setFullUpdate(self):
        with self._lock:
            self._display.init(self._display.FULL_UPDATE)
            self._is_full_update = True
            
    def _setPartUpdate(self):
        with self._lock:
            self._display.init(self._display.PART_UPDATE)
            self._is_full_update = False
        
    def initialize(self):
        logging.info("initializing waveshare v2 display")
        from pwnagotchi.ui.hw.libs.waveshare.v2.waveshare import EPD
        self._display = EPD()
        self.clear()

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        with self._lock:
            if self._is_full_update:
                self._display.display(buf)
                self._setPartUpdate()
            else:
                self._display.displayPartial(buf)

    def clear(self):
        self._setFullUpdate()
