import logging
import babel
import babel.dates

import weather
import drawing


EPD_WIDTH = 400
EPD_HEIGHT = 300

# only update once an hour within these ranges
DEAD_TIMES = [
    range(0,6),
    range(10,16)
]

class PaperClock( object ):

    def __init__( self, debug_mode=False ):
        
        self._debug_mode = debug_mode
        if not debug_mode:
            import epd4in2
            self._epd = epd4in2.EPD()
            self._epd.init()
        
        self._str_time = "XXXX"


    def display_buffer( self, buf ):
        
        if self._debug_mode:
            buf.save( "debug.bmp" )
            return
        
        self._epd.display_frame(
            self._epd.get_frame_buffer( buf )
        )


    def update_for_datetime( self, dt ):

        tz_display = babel.dates.get_timezone('Europe/London')
        formatted = babel.dates.format_time(
            dt,
            "HHmm",
            tzinfo=tz_display
        )

        # set blank minutes if time's hour is within dead ranges
        h = int(formatted[:2])
        for dead_range in DEAD_TIMES:
            if h in dead_range:
                formatted = "{}  ".format( h )

        if formatted != self._str_time:

            w = weather.get_weather()

            frame = drawing.draw_frame(
                EPD_WIDTH, EPD_HEIGHT,
                formatted,
                w
            )
            self.display_buffer( frame )
            
            self._str_time = formatted