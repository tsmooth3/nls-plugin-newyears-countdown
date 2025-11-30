# New Years Counter Downer Board

A **New Years Countdown Board** for the [NHL LED Scoreboard](https://github.com/falkyre/nhl-led-scoreboard) that displays a countdown to New Year's Day.

This board shows:
- Days remaining until New Year's Day
- Hours, minutes, and seconds countdown
- New Year's Eve ball image
- Special "Happy New Year!" scrolling display on New Year's Day

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Display Modes](#display-modes)
- [How It Works](#how-it-works)

---

## Features

- Real-time countdown to New Year's Day (January 1st)
- Displays days, hours, minutes, and seconds until New Year's Day
- New Year's Eve ball image display
- Special New Year's Day celebration mode with scrolling "HAPPY NEW YEAR!" message and ball graphic
- Automatically handles year rollover (counts down to next New Year's Day)
- Extended display time when "almost there" (less than 10 minutes remaining)
- Only displays when 33 days or fewer until New Year's Day

---

## Installation

1. Use the NHL Led Scoreboard's plugin manager python script to install:

   ```bash
   python plugins.py add https://github.com/tsmooth3/nls-plugin-newyears-board.git
   ```

2. Add `newyears_board` to your NHL-LED-Scoreboard's main configuration:

   ```bash
   nano config/config.json
   ```

   For example, to add it to the off day rotation:

   ```json
   "states": {
       "off_day": [
           "season_countdown",
           "newyears_board",
           "team_summary",
           "scoreticker",
           "clock"
       ]
   }
   ```

   **Note:** You must restart the scoreboard for changes to take effect.

---

## Configuration

The New Years Counter Downer board requires no additional configuration. It uses the standard scoreboard fonts and layout settings from your main configuration.

---

## Display Modes

The board has two main display modes:

### Countdown Mode (Days 33 to 1)

When there are 1-33 days until New Year's Day, the board displays:
- Days remaining (e.g., "25 days")
- Time remaining in HH:MM:SS format
- New Year's Eve ball image (48x48 pixels)
- "'TIL {year}" text at the bottom showing the target year

The board loops for 10 iterations (10 seconds) normally, or 180 iterations (3 minutes) when "almost there" (less than 600 seconds / 10 minutes remaining).

### New Year's Day Mode

On January 1st, the board displays:
- Scrolling "{previous_year} HAPPY NEW YEAR! {previous_year}" text in yellow/cream color
- New Year's Eve ball graphic following the text
- Continuous scrolling animation for 45 seconds
- Special celebration display

---

## How It Works

1. The board calculates the time remaining until the next New Year's Day (January 1st)
2. It handles year rollover automatically - if the current date is after January 1st, it counts down to next year's New Year's Day
3. The countdown updates in real-time, showing:
   - Total days remaining
   - Hours, minutes, and seconds remaining
4. When there are 33 days or fewer until New Year's Day, the countdown display is shown
5. When less than 600 seconds (10 minutes) remain, the board enters "almost there" mode with extended display time (180 seconds instead of 10 seconds)
6. On New Year's Day itself, the board switches to celebration mode with scrolling "HAPPY NEW YEAR!" text and ball graphic for 45 seconds
7. The board uses the following fonts from your scoreboard configuration:
   - `font_large_2` for large text
   - `font_medium` for medium text
   - `font_xmas` for scrolling New Year's text

The board automatically updates the countdown each second and refreshes the display accordingly.
