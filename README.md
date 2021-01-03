# thread_switcher
Tool to force a single-threaded benchmark tool to switch to a different core periodically.
Useful if you are playing with curve optimizer on Ryzen 5000 processors.
This allows you to test the stability of different cores separately.

# Get started
Download the files in this repository and put them in the same folder.
To run the tool, install Python 3.9 from the Microsoft Store then simply double-click run.bat and the tool will keep trying to switch prime95 to a different core.
To change the settings (such as which process (prime95 or something else) to switch and how often and your number of cores,
open main.py with a textm editor and edit the configuration at the top of the file.
You have to close and restart the tool for the changes to take effect.

# Compatibility
This tool was only tested on Windows 10 and will not run on Linux without changes.

# But how do I overclock Zen 3 / Ryzen 5000?
I can recommend this guide: https://www.reddit.com/r/Amd/comments/khtx1o/guide_zen_3_overclocking_using_curve_optimizer/
