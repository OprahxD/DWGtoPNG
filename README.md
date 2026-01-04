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
from DWGtoPNG import batch_convert_folder



if __name__ == "__main__":
    # Change to the correct input and output folders with dwg files:
    source_folder = r"C:\Users\input_data"
    output_folder = r"C:\Users\output_data"
    # The last input is the DPI - Higher the number, clearer the PNG
    batch_convert_folder(source_folder,output_folder,300)
    print("Starting batch conversion")
    
