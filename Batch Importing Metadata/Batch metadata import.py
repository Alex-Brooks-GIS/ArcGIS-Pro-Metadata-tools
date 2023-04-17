import os
import arcpy
from arcpy import metadata as md

# Set your workspace
workspace = r"Raster directory" #update before use
metadata_dir = r"Metadata directory" #update before use
arcpy.env.workspace = workspace

# Get a list of raster images in the workspace
rasters = arcpy.ListRasters()

if rasters:
    print("Rasters found:" + str(rasters))
    
    # Iterate through each raster
    for raster in rasters:
        # Skip raster if it has the .aux extension
        if raster.lower().endswith('.aux'):
            continue
    
        # Construct the XML file name
        xml_file = f"{raster}.xml"
    
        # Check if the XML file exists in the metadata directory
        if os.path.exists(os.path.join(metadata_dir, xml_file)):
            # Get the target raster's Metadata object
            tgt_raster_md = md.Metadata(raster)
    
            # Import the metadata content from the XML file to the target raster
            if not tgt_raster_md.isReadOnly:
                tgt_raster_md.importMetadata(os.path.join(metadata_dir, xml_file))
                tgt_raster_md.save()
                print(f"Imported metadata for {raster}")
        else:
            print(f"Metadata not found for {raster}")
else:
    print("No rasters found in the specified workspace.")
