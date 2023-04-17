# Importing necessary modules
import os
import csv

# Define the directory path where the CSV and template files are stored
directory = r"Output Directory"

# Create the absolute paths to the CSV and template files
csv_file = os.path.join(directory, "data.csv")
template_file = os.path.join(directory, "template.txt")

# Loop through the data and populate the template with each row
for row in csv.DictReader(open(csv_file)):
    # Read the template file and replace placeholders with data
    with open(template_file, 'r') as file:
        template = file.read()

    # Replace the placeholders in the template with the corresponding values from the row
    message = template.replace('{{<idAbs></idAbs>}}', row['<idAbs></idAbs>'])
    message = message.replace('{{<createDate></createDate>}}', row['<createDate></createDate>'])
    message = message.replace('{{<reviseDate></reviseDate>}}', row['<reviseDate></reviseDate>'])
    message = message.replace('{{<resTitle><date>}}', row['<resTitle><date>'])
    message = message.replace('{{<value uom="m"></value>}}', row['<value uom="m"></value>'])
    # message = message.replace('{{<dataExt></dataExt>}}', row['<dataExt></dataExt>'])
    message = message.replace('{{<keyword></keyword>}}', row['<keyword></keyword>'])
    
    # Write the XML content to a new file
    output_file = os.path.join(directory, f"{row['File Name']}")
    with open(output_file, 'w') as file:
        file.write(message)

    # Print the filename of the new file
    print(f"Created file {output_file}")
