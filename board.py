"""
New Years Counter Downer board module implementation.
"""
import datetime
import logging
import os

from PIL import Image
from boards.base_board import BoardBase
from data.data import Data
from renderer.matrix import Matrix

from . import __board_name__, __description__, __version__

debug = logging.getLogger("scoreboard")

# ---- Main class --------------------------------------------------------------
class NewYears(BoardBase):
    """
    The **New Years Counter Downer** displays a countdown to New Years.
    """

    def __init__(self, data: Data, matrix: Matrix, sleepEvent):
        super().__init__(data, matrix, sleepEvent)

        # Board metadata from package
        self.board_name = __board_name__
        self.board_version = __version__
        self.board_description = __description__
        
        # Get configuration values with defaults
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()

        # Resolve paths relative to the plugin directory
        self.board_dir = self._get_board_directory()

        # Access standard application config
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.medium = data.config.layout.font_medium
        self.font.scroll = data.config.layout.font_xmas
        self.scroll_pos = self.matrix.width

        # custom variables
        self.almost_there = False
        self.new_year = 0
        self.days_to_ny = 0
        self.hours_to_ny = 0
        self.minutes_to_ny = 0
        self.seconds_to_ny = 0

    def _get_board_directory(self):
        """Get the absolute path to this board's directory."""
        import inspect
        board_file = inspect.getfile(self.__class__)
        return os.path.dirname(os.path.abspath(board_file))

    # -------- Rendering --------
    def render(self):
        debug.info("Rendering New Years Counter Downer")

        self.matrix.clear()

        self.update_countdown()

        if self.days_to_ny == 364:
            #today is New Years
            self.ny_today()
        else:
            #today is not New Years
            if self.days_to_ny <= 33: 
                self.ny_countdown()

    def update_countdown(self):

        #get today's date
        today = datetime.datetime.now()
        
        # for testing
        now = datetime.datetime.now()
        td = datetime.timedelta(days=15, hours=2, minutes=17)
        #today = now + td
        
        #find the next new years year
        new_year = today.year + 1

        ny = datetime.datetime(new_year,1,1)
        
        #calculate days to new years
        time_to_ny = ny - today
        self.new_year = new_year
        self.days_to_ny = time_to_ny.days
        self.hours_to_ny = time_to_ny.seconds // 3600
        self.minutes_to_ny = (time_to_ny.seconds % 3600) // 60
        self.seconds_to_ny = time_to_ny.seconds % 60
        if time_to_ny.total_seconds() < 600:
            self.almost_there = True
        else:
            self.almost_there = False

        debug.info(f"New Years Countdown: {self.almost_there} : {self.days_to_ny:02}d {self.hours_to_ny:02}h {self.minutes_to_ny:02}m {self.seconds_to_ny:02}s")
    
    def ny_today(self) :
        #  it's New Years!

        duration = 45
        i = 0
        scroll_rate = .01
            
        debug.info("Happy New Year!")

        while not self.sleepEvent.is_set():

            self.matrix.clear()

            ny_scroll_text = self.matrix.draw_text(
                (self.scroll_pos,12),
                f"{self.new_year - 1} HAPPY NEW YEAR! {self.new_year - 1}  ",
                font=self.font.scroll,
                fill=(255,255,200)
                )
            
            ny_scroll_text_width = ny_scroll_text["size"][0] + 3
            
            ny_image = Image.open(f'{self.board_dir}/assets/images/nye-ball.jpg').resize((48,48))
            self.matrix.draw_image((self.scroll_pos + ny_scroll_text_width,4), ny_image)

            ny_content_width = ny_scroll_text_width + 48

            if(self.scroll_pos < (0 - ny_content_width) ): self.scroll_pos = self.matrix.width

            i += scroll_rate
            self.scroll_pos -= 1

            self.matrix.render()
            self.sleepEvent.wait(scroll_rate)

            if(i > duration) : break

    def ny_countdown(self) :
        
        debug.info("New Years Counter Downer")
        loopTime = 10
        if self.almost_there: 
            loopTime = 180
        
        for _ in range(loopTime):
            self.update_countdown()
            
            self.matrix.clear()
            if self.days_to_ny == 364:
                self.almost_there = False
                self.ny_today()
                break

            #draw countdown to new years
            self.matrix.draw_text(
                (10,10),
                f"{self.days_to_ny} days",
                font=self.font.medium,
                fill=(200,255,200)
            )
            self.matrix.draw_text(
                (10,23),
                f"{self.hours_to_ny:02}:{self.minutes_to_ny:02}:{self.seconds_to_ny:02}",
                font=self.font.medium,
                fill=(200,255,200)
            )
        
            #choose one of three daily images to draw based on days to new years and draw it
            ny_image = Image.open(f'{self.board_dir}/assets/images/nye-ball.jpg').resize((48,48))

            self.matrix.draw_image((75,2), ny_image)
           

            self.matrix.draw_text(
                (15,45), 
                f"'TIL {self.new_year}", 
                font=self.font.medium,
                fill=(255,255,100)
            )
            
            self.matrix.render()
            self.sleepEvent.wait(1)