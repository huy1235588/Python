import os
import sys

from utils.initGui import CaldendarWindow

cur_path = sys.path[0]

gui = CaldendarWindow(cur_path)

gui.start()
