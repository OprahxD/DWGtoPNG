Copy the following code and paste in the file you want to use, also make sure you have the correct imports at too.
You will also need ODA converter and remember it's path as you will have to put it in the module.
Type this to install ODA converter:
$ sudo dpkg -i ODAFileConverter_25.12.0.0_Linux_x86_64.deb
Then this to get the file path
$ which ODAFileConverter






import matplotlib
matplotlib.use('Agg') 

import os
import matplotlib.pyplot as plt 
from DWGtoPNG import convert_dwg_to_png


if __name__ == "__main__":
    source_file = r"C:\Users\shres\OneDrive\Desktop\Python\dwgToPng\input_data\input2.dwg"
    DPI = 300
    convert_dwg_to_png(source_file,DPI)
    
