import sys
import os
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ezdxf
import platform
from ezdxf.addons.drawing import RenderContext, Frontend
import time
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

# --- CONFIGURATION ---
# 1. Path to ODA Converter (Points to Executable)

def get_default_oda_path():
    """Detects OS and returns standard ODA installation path."""
    current_os = platform.system()
    if current_os == "Windows":
        # Check specific version (Update this if you upgrade ODA)
        return r"C:\Program Files\ODA\ODAFileConverter\ODAFileConverter.exe"
    elif current_os == "Linux":
        return r'/usr/bin/ODAFileConverter'
    elif current_os == "Darwin":
        return "/Applications/ODAFileConverter.app/Contents/MacOS/ODAFileConverter"
    return None
# 2. Output Settings
ODA_PATH = get_default_oda_path()
# OUTPUT_DPI = 600  # Higher DPI = "High Res Screenshot"

def convert_dwg_to_png(dwg_path, OUTPUT_DPI):
    

    
    base_dir = os.path.dirname(os.path.abspath(dwg_path))
    filename = os.path.basename(dwg_path)
    filename_no_ext = os.path.splitext(filename)[0]
    
    # Define Output Path (Same folder as input, same name, .png extension)
    output_png_path = os.path.join(base_dir, f"{filename_no_ext}.png")
    # output_png_path = output_path
    
    temp_dir = os.path.join(base_dir, "temp_render")
    
    # 1. CLEANUP & PREP
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    print(f"--- Processing: {dwg_path} ---")

    # 2. CONVERT DWG -> DXF (Using ODA)
    # We use ODA because Python cannot natively read DWG files reliably.
    print("Step 1: Converting DWG to DXF (geometry extraction)...")
    oda_cmd = [
        ODA_PATH,
        base_dir,       # Input Folder
        temp_dir,       # Output Folder
        "ACAD2010",     # Version 2010 is a sweet spot for compatibility
        "DXF",          # Type
        "0", "0"        # Recurse, Audit
    ]

    # 1. Initialize as None (Safe for Linux/Mac)
    startupinfo = None
        
        # 2. Only add Windows-specific flags IF we are on Windows
    if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        # 3. Run the command
        # Passing 'startupinfo=None' on Linux is perfectly fine and safe.
    subprocess.run(
            oda_cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo
        )

# 3. Run with the hidden flag
    subprocess.run(
        oda_cmd, 
        capture_output=True, 
        startupinfo=startupinfo  # <--- THIS IS THE KEY
    )
    
    # Run ODA
    
    
    # Find the generated DXF
    filename = os.path.splitext(os.path.basename(dwg_path))[0]
    dxf_path = os.path.join(temp_dir, f"{filename}.dxf")
    
    if not os.path.exists(dxf_path):
        print("❌ CRITICAL: DXF file was not created. Check ODA path.")
        return

    # 3. RENDER DXF -> PNG (The "Virtual Screenshot" Step)
    print("Step 2: Rendering geometry to Image (Matplotlib)...")
    
    try:
        # Load DXF document
        doc = ezdxf.readfile(dxf_path)
        
        # Prepare the "Virtual Canvas" (Model Space)
        msp = doc.modelspace()
        
        # Setup the render context (handles colors, line weights)
        ctx = RenderContext(doc)
        
        # Setup the Plot (The "Camera")
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        
        # The Frontend orchestrates the drawing
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        
        # Save the "Screenshot"
        print(f"Saving high-res PNG to: {output_png_path}")
        fig.savefig(output_png_path, dpi=OUTPUT_DPI)
        
        # Close the plot to free memory
        plt.close(fig)
        print("✅ Success! Conversion Complete.")

        return output_png_path
        
    except Exception as e:
        print(f"❌ Render Error: {e}")
        
    # Optional: Cleanup temp DXF
    # import shutil
    # shutil.rmtree(temp_dir)


def batch_convert_folder(source_folder, output_folder, dpi=300):
    """
    Scans source_folder for DWG files and converts them to PNGs in output_folder.
    """
    
    # 1. Setup Folders
    if not os.path.exists(source_folder):
        print(f"❌ Error: Source folder not found: {source_folder}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # 2. Get List of DWG Files
    all_files = os.listdir(source_folder)
    dwg_files = [f for f in all_files if f.lower().endswith('.dwg')]
    
    total_files = len(dwg_files)
    if total_files == 0:
        print("No .dwg files found in this folder.")
        return

    print(f"🚀 Starting Batch Conversion: {total_files} files found.")
    print("-" * 50)

    # 3. Loop and Convert
    success_count = 0
    start_time = time.time()

    for index, filename in enumerate(dwg_files):
        # Construct full file paths
        input_path = os.path.join(source_folder, filename)
        
        # We want the output filename to be "floorplan.png" inside the output folder
        output_filename = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(output_folder, output_filename)

        print(f"[{index + 1}/{total_files}] Converting: {filename} ...")

        # CALL THE IMPORTER
        result = convert_dwg_to_png(input_path, output_path,dpi)
        
        if result:
            success_count += 1
        else:
            print(f"   ⚠️ Failed to convert: {filename}")

    # 4. Final Report
    elapsed = time.time() - start_time
    print("-" * 50)
    print(f"🏁 Batch Complete!")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed:     {total_files - success_count}")
    print(f"⏱️ Time Taken: {elapsed:.2f} seconds")
