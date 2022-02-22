# thread_switcher

Tool to force a benchmark tool to switch to a different core periodically.
Useful if you are playing with curve optimizer on Ryzen 5000 processors.
This allows you to test the stability of different cores separately.

## Get started

Download the files in this repository and put them in the same folder.
To run the tool, install Python >= 3.9 from [python.org](https://www.python.org) then simply double-click main.py (or run.bat) and the tool will keep trying to switch prime95 to a different core.

**DO NOT FORGET TO ADJUST YOUR SETTINGS**:
open the relevant settings file, either `settings_prime95.py` or `settings_aida64.py` with a text editor and edit the necessary settings in the ###.

You have to close and restart the tool for the changes to take effect.

For running thread switcher with AIDA64, you need to also modify `settings_aida64.py`. Note, this bat must be run as admin.
- To always run `run_thread_switcher_aida64.bat` admin, you may:
1. Create a shortcut to `run_thread_switcher_aida64.bat`
2. Right-click -> properties -> shortcut tab -> advanced -> enable "Run as administrator"

## NOTE ABOUT NEW VERSION AS OF March 2021:

The core now loads a full physical core, which for most of you, notably those running 5600X, 5800X, 5900X or 5950X CPU's, will be 2 threads.
So make sure to run prime95 with at least 2 threads now when using this tool, **NOT SINGLE-THREADED**, for maximum stress on a single physical CPU core.

## Compatibility

This tool was only tested on Windows 10 and will not run on Linux without changes.

## But how do I overclock Zen 3 / Ryzen 5000?

I can recommend this guide: <https://www.reddit.com/r/Amd/comments/khtx1o/guide_zen_3_overclocking_using_curve_optimizer/>
