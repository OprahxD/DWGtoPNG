Copy the following code and paste in the file you want to use, also make sure you have the correct imports at too, they are available in the requirements.txt file.
You will also need ODA converter and remember it's path as you will have to put it in the module.
Go to this website and download the ODAFileConverter file:
https://www.opendesign.com/guestfiles/oda_file_converter
Then run:
sudo gdebi ODAFileConverter_QT6_lnxX64_8.3dll_26.10.deb
Then this to get the file path:
which ODAFileConverter
Put the file path in the DWGtoPNG module.


Use this code to run:

import matplotlib
matplotlib.use('Agg') 

import os
import matplotlib.pyplot as plt 
from DWGtoPNG import convert_dwg_to_png


if __name__ == "__main__":
    source_file = r"C:\Users\shres\OneDrive\Desktop\Python\dwgToPng\input_data\input2.dwg"
    DPI = 300
    convert_dwg_to_png(source_file,DPI)
    
