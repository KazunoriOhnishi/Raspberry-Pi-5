#  Pi_Ondo.py

import os
temp = os.popen("vcgencmd measure_temp") . read ( )
print("CPU temperature:", temp)
