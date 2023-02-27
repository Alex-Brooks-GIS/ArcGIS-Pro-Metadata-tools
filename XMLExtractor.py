import os
import csv

directory_path = r'Search Directory path'
output_path = r'Output Directory\data.csv'
failed_export_path = r'Output Directory\failedexport.csv'
tag_pairs = [('<idAbs>', '</idAbs>'), ('<createDate>', '</createDate>'), ('<reviseDate>', '</reviseDate>'), ('<resTitle>', '<date>'), ('<value uom="m">', '</value>'), ('<dataExt>', '</dataExt>'),('<keyword>', '</keyword>')]

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
                    else:
                        text_to_read = ''
                        print(f'Error: could not find second occurrence of {start_tag + end_tag} in {file_name}')
                extracted_data[tag_pair_index] = text_to_read
            else:
                print(f'Error: could not find start and/or end tag {start_tag + end_tag} in {file_name}')
            tag_pair_index += 1
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