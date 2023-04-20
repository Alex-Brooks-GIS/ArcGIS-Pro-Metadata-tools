import arcpy
import os
import csv
# Additional imports if needed

class Toolbox(object):
    def __init__(self):
        self.label = "Combined Toolbox"
        self.alias = "combined_toolbox"
        self.tools = [ExportMetadata, CSVtoXML, ImportMetadata]

# Define the custom geoprocessing tool class
class ExportMetadata(object):
    def __init__(self):
        self.label = "Export XML Metadata to CSV"
        self.description = "Exports metadata from XML files into a CSV file."
        self.canRunInBackground = False

    # Define the input parameters for the geoprocessing tool
    def getParameterInfo(self):
        directory_path_param = arcpy.Parameter(
            displayName="XML Directory Path",
            name="directory_path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        output_path_param = arcpy.Parameter(
            displayName="Data Output Path",
            name="output_path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        failed_export_path_param = arcpy.Parameter(
            displayName="Failed Export Path",
            name="failed_export_path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [directory_path_param, output_path_param, failed_export_path_param]
        return params

    # Define the execution logic for the geoprocessing tool
    def execute(self, parameters, messages):
        directory_path = parameters[0].valueAsText
        output_path = os.path.join(parameters[1].valueAsText, "data.csv")
        failed_export_path = os.path.join(parameters[2].valueAsText, "failedexport.csv")

        tag_pairs = [('<idAbs>', '</idAbs>'), ('<createDate>', '</createDate>'), ('<resTitle>', '<date>'), ('<value uom="m">', '</value>'), ('<dataExt>', '</dataExt>'), ('<keyword>', '</keyword>'), ('<rpIndName>', '</rpIndName>)'), ('<rpPosName>', '</rpPosName>'), ('<rpOrgName>', '</rpOrgName>')]

        header_row = ['File Name']
        for start_tag, end_tag in tag_pairs:
            header_row.append(start_tag + end_tag)
        with open(output_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header_row)
        with open(failed_export_path, 'w', newline='') as failed_export_file:
            writer = csv.writer(failed_export_file)
            writer.writerow(['File Name'])

        for file_name in os.listdir(directory_path):
            if file_name.lower().endswith('.xml') and not file_name.lower().endswith('.aux'):
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()

                # Add these lines to ignore content between <Thumbnail></Thumbnail>
                start_thumbnail_index = content.find('<Thumbnail>')
                end_thumbnail_index = content.find('</Thumbnail>')
                if start_thumbnail_index != -1 and end_thumbnail_index != -1:
                    content = content[:start_thumbnail_index] + content[end_thumbnail_index+len('</Thumbnail>'):]

                extracted_data = [''] * len(tag_pairs)
                tag_pair_index = 0
                while tag_pair_index < len(tag_pairs):
                    start_tag, end_tag = tag_pairs[tag_pair_index]
                    start_index = content.find(start_tag)
                    end_index = content.find(end_tag)
                    if start_index < end_index:
                        text_to_read = content[start_index+len(start_tag):end_index]
                        if start_tag == '<value uom="m">' and end_tag == '</value>' or start_tag == '<keyword>' and end_tag == '</keyword>':
                            # Write all occurrences of the tag pair split by a comma and append a capital "M" (for value uom="m")
                            occurrences = []
                            while start_index != -1 and end_index != -1:
                                if start_tag == '<value uom="m">' and end_tag == '</value>':
                                    occurrences.append(text_to_read + " m")
                                else:
                                    occurrences.append(text_to_read)
                                start_index = content.find(start_tag, end_index + 1)
                                end_index = content.find(end_tag, end_index + 1)
                                if start_index < end_index:
                                    text_to_read = content[start_index+len(start_tag):end_index]
                            text_to_read = ', '.join(occurrences)
                        elif start_tag == '<resTitle>' and end_tag == '<date>':
                            # Only write values on the second occurrence of the tag pair
                            second_occurrence_start_index = content.find(start_tag, end_index + 1)
                            second_occurrence_end_index = content.find(end_tag, end_index + 1)
                            if second_occurrence_start_index < second_occurrence_end_index:
                                text_to_read = content[second_occurrence_start_index+len(start_tag):second_occurrence_end_index]
                                text_to_read = text_to_read.replace("</resTitle>", "")  # remove "</resTitle>" tag
                            else:
                                text_to_read = ''
                                arcpy.AddWarning(f'Error: could not find second occurrence of {start_tag + end_tag}')
                        extracted_data[tag_pair_index] = text_to_read
                    else:
                        arcpy.AddWarning(f'Error: could not find start and/or end tag {start_tag + end_tag} in {file_name}')
                    tag_pair_index += 1
                if any(extracted_data):
                    with open(output_path, 'a', newline='') as output_file:
                        writer = csv.writer(output_file)
                        writer.writerow([file_name] + extracted_data)
                        arcpy.AddMessage([file_name] + extracted_data)
                else:
                    with open(failed_export_path, 'a', newline='') as failed_export_file:
                        writer = csv.writer(failed_export_file)
                        writer.writerow([file_name])
                        arcpy.AddWarning(f'Error: could not extract data from {file_name}')

class CSVtoXML(object):
    def __init__(self):
        self.label = "CSV to XML Converter"
        self.description = "Converts a CSV file into XML files using a template file."
        self.canRunInBackground = False

    def getParameterInfo(self):
        csv_file_param = arcpy.Parameter(
            displayName="data.csv File",
            name="csv_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        template_file_param = arcpy.Parameter(
            displayName="Template.txt File",
            name="template_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        output_directory_param = arcpy.Parameter(
            displayName="XML Output Directory",
            name="output_directory",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [csv_file_param, template_file_param, output_directory_param]
        return params

    def execute(self, parameters, messages):
        csv_file = parameters[0].valueAsText
        template_file = parameters[1].valueAsText
        output_directory = parameters[2].valueAsText

        for row in csv.DictReader(open(csv_file)):
            with open(template_file, 'r') as file:
                template = file.read()

            message = template.replace('{{<idAbs></idAbs>}}', row['<idAbs></idAbs>'])
            message = message.replace('{{<createDate></createDate>}}', row['<createDate></createDate>'])
            message = message.replace('{{<resTitle><date>}}', row['<resTitle><date>'])
            message = message.replace('{{<value uom="m"></value>}}', row['<value uom="m"></value>'])
            message = message.replace('{{<keyword></keyword>}}', row['<keyword></keyword>'])
            message = message.replace('{{<rpOrgName></rpOrgName>}}', row['<rpOrgName></rpOrgName>'])
            message = message.replace('{{<rpPosName></rpPosName>}}', row['<rpPosName></rpPosName>'])
            message = message.replace('{{<rpIndName></rpIndName>)}}', row['<rpIndName></rpIndName>)'])

            output_file = os.path.join(output_directory, f"{row['File Name']}")
            with open(output_file, 'w') as file:
                file.write(message)

            arcpy.AddMessage(f"Created file {output_file}")

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

