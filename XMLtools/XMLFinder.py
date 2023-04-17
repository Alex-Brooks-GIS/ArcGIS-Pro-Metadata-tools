import os
import csv

def export_xml_files(directory, csv_file_path):
    xml_files = []

    for filename in os.listdir(directory):
        if filename.endswith(".xml") and not (".aux" in filename):
            xml_files.append(filename)

    if xml_files:
        with open(csv_file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["XML Files"])
            writer.writerows([[xml_file] for xml_file in xml_files])

        print(f"List of xml files has been stored in {csv_file_path}.")
    else:
        print("No xml files found in the directory.")

# Assign the directory path directly
directory = r'Search Directory path'
csv_file_path = r'Output Directory\xml_files.csv'

# Call the function with the imported directory path
export_xml_files(directory, csv_file_path)
