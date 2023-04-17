import os
import arcpy
from arcpy import metadata as md

# Define the custom toolbox class
class Toolbox(object):
    def __init__(self):
        self.label = "Metadata Import Toolbox"
        self.alias = "metadata_import_toolbox"
        self.tools = [ImportMetadata]

# Define the custom geoprocessing tool class
class ImportMetadata(object):
    def __init__(self):
        self.label = "Import Raster Metadata"
        self.description = "Imports metadata from XML files to corresponding raster files in the workspace."
        self.canRunInBackground = False

    # Add a description for the entire geoprocessing tool
    __doc__ = """
    This tool is designed to import metadata from XML files to their corresponding raster files within a specified workspace.
    
    The tool requires two input parameters:
    1. Workspace: Provide the directory containing the raster files for which metadata needs to be imported.
    2. Metadata Directory: Provide the directory containing the XML metadata files corresponding to the raster files.
    
    The tool will iterate through all raster files in the workspace and import metadata from XML files with matching names. If metadata is not found for a raster file, a warning will be displayed in the Geoprocessing Messages.
    """

    # Define the input parameters for the geoprocessing tool
    def getParameterInfo(self):
        workspace_param = arcpy.Parameter(
            displayName="Raster Directory",
            name="workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        metadata_dir_param = arcpy.Parameter(
            displayName="Metadata Directory",
            name="metadata_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [workspace_param, metadata_dir_param]
        return params

    # Define the execution logic for the geoprocessing tool
    def execute(self, parameters, messages):
        # Get the input parameter values
        workspace = parameters[0].valueAsText
        metadata_dir = parameters[1].valueAsText

        # Set the arcpy workspace
        arcpy.env.workspace = workspace

        # List all rasters in the workspace
        rasters = arcpy.ListRasters()

        # Check if rasters are found
        if rasters:
            arcpy.AddMessage("Rasters found:" + str(rasters))

            # Iterate through the rasters
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
                        arcpy.AddMessage(f"Imported metadata for {raster}")
                else:
                    arcpy.AddWarning(f"Metadata not found for {raster}")
        else:
            arcpy.AddError("No rasters found in the specified workspace.")
