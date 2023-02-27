import os
import csv

directory_path = r'Search Directory'
output_path = r'Output Directory\output.csv'
failed_export_path = r'Output Directory\failedexport.csv'

tag_pairs = {'Product Type': 'Source',
             'Source': 'Source Unit',
             'Source Unit': 'Product Class',
             'Product Class': 'NIIRS',
             'NIIRS': 'Acquisition Date',
             'Acquisition Date': 'Ingest Date',
             'Ingest Date': 'Age In Days',
             'Age In Days': 'Cloud Cover',
             'Cloud Cover': 'Has Cloudless Geometry',
             'Has Cloudless Geometry': 'Show Browse Image',
             'Show Browse Image': 'Off Nadir Angle',
             'Off Nadir Angle': 'Sun Elevation',
             'Sun Elevation': 'Sun Azimuth',
             'Sun Azimuth': 'Feature Id',
             'Feature Id': 'Legacy Identifier',
             'Legacy Identifier': 'Legacy Description',
             'Legacy Description':'Factory Order Number',
             'Factory Order Number':'Data Layer',
             'Data Layer':'Acquisition Type',
             'Acquisition Type':'Sensor Type',
             'Sensor Type':'Orbit Direction',
             'Orbit Direction':'Crs From Pixels',
             'Crs From Pixels':'Precise Geometry',
             'Precise Geometry':'Per Pixel',
             'Per Pixel':'Per Pixel Y',
             'Per Pixel Y':'CE90 Accuracy',
             'CE90 Accuracy':'RMSE Accuracy',
             'RMSE Accuracy':'Spatial Accuracy',
             'Spatial Accuracy':'Company Name',
             'Company Name':'Vendor Name',
             'Vendor Name':'Vendor Reference',
             'Vendor Reference':'Copyright',
             'Copyright':'License Type',
             'License Type':'Security Classification',
             'Security Classification':'2'}

header_row = ['File Name']
for start_tag in tag_pairs:
    header_row.append(start_tag)

with open(output_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header_row)

with open(failed_export_path, 'w', newline='') as failed_export_file:
    writer = csv.writer(failed_export_file)
    writer.writerow(['File Name'])

for file_name in os.listdir(directory_path):
    if file_name.lower().endswith('.txt') and not file_name.lower().endswith('.aux'):
        file_path = os.path.join(directory_path, file_name)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except:
            print(f'Error: could not open file {file_name}')
            continue
        extracted_data = []
        for start_tag in tag_pairs:
            end_tag = tag_pairs[start_tag]
            start_index = content.find(start_tag)
            end_index = content.find(end_tag, start_index)
            if start_index != -1 and end_index != -1:
                text_to_read = content[start_index + len(start_tag):end_index].strip()
                extracted_data.append(text_to_read)
            else:
                extracted_data.append('')
                print(f'Error: could not find start and/or end tag {start_tag} - {end_tag} in {file_name}')
        if any(extracted_data):
            with open(output_path, 'a', newline='') as output_file:
                writer = csv.writer(output_file)
                writer.writerow([file_name] + extracted_data)
                print([file_name] + extracted_data)
        else:
            with open(failed_export_path, 'a', newline='') as failed_export_file:
                writer = csv.writer(failed_export_file)
                writer.writerow([file_name])
                print(f'Error: could not extract data from {file_name}')
