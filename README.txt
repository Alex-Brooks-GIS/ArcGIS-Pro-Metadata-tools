This repository is comprised of three python scripts which I have created to perform three main actions. 

Action 1: Identify existing metadata within a given file directory. 

This script works by going through the defined directory and idenifying each of the files with a .xml file extension, the script excludes files with a .aux.xml extension as these do not contain metadata beyond summary statistics

Action 2: Extract key components the old metadata to a csv folder.

The script works by hunting through each of the .xml files within a given directory and looks to find tag pairs from which key information like, Item description, title, resolution, keywords, creation date, revision date and data extent are housed.

Action 3: Use the extracted metadata to populate an upto date XML metadata template that is ISO 19115 compliant 

The last script works by using the output from the extractor script and populate a static template using a replace function on specific tags.

Please note: that the second action has limited error handling, thus some manual clean-up in excel might be required.
When running the 3rd script (XMLTemplateupdater) you will require the template.txt and data.csv to be housed within the same directory.
