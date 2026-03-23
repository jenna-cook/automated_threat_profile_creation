# Title: threat_profile.py
# Author: Jenna Cook
# Description: A threat profile of a cybercriminal
# organization is produced.
# Input: Set the CYBERCRIMINAL_ORG, SCRAPING_FUNC,
# GENAI_API_KEY, OPENCTI_API_KEY, and
# OPENCTI_INSTANCE environment variables.
# Output: A threat profile is produced called
# {CYBERCRIMINAL_ORG}_threat_profile.md where CYBERCRIMINAL_ORG
# is the name of the cybercriminal organization the threat profile
# is about. This file should be in a directory that is named after
# the cybercriminal organization.

import os
import scrape
import description
import cti
import sorting
import chart
from datetime import datetime

# Track the start time, so the amount of time the script runs can be calculated
start_time = datetime.now()
formatted_date = start_time.strftime("%B %d, %Y")
formatted_time = start_time.strftime("Start time: %H:%M:%S")
cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
scraping_func = os.getenv("SCRAPING_FUNC")
# Create a directory to put all the files in
dir_path = f"./{cybercriminal_org}"
os.makedirs(dir_path, exist_ok=True)
with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "w") as time_file:
    time_file.write("Start creating threat profile...\n")
    time_file.write(f"{formatted_time}\n")
    time_file.close()

# Use the scraping function defined in SCRAPING_FUNC
scraping = getattr(scrape, scraping_func)
# Scrape a DLS
scraping()
# Categorize victims by NAICS
sorting.sort()
# Produce a bar chart showing the number of victims 
# in each NAICS sector
chart.create_chart()

# Add the title and date to the threat profile 
with open(f"{dir_path}/{cybercriminal_org}_threat_profile.md", "w") as f:
    f.write(f"# {cybercriminal_org} Threat Profile\n")
    f.write(f"### Date: {formatted_date}\n\n")
    f.close()

# Produce a description of the cybercriminal organization and
# add it to the threat profile
description.describe_org()

# Add the bar chart to the threat profile
with open(f"{dir_path}/{cybercriminal_org}_threat_profile.md", "a") as f:
    chart_path = f"./{cybercriminal_org}_barchart.png"
    chart_path_url_encoded_space = chart_path.replace(" ", "%20")
    f.write(f'\n\n## Industry Targeting !["{cybercriminal_org} Victims Categorized By NAICS"]("{chart_path_url_encoded_space}")\n')
    f.close()

# Aggregate CTI and add the tables of information and descriptions in the threat profile
cti.get_cti()

# Track the end time, so the amount of time the script runs can be calculated
end_time = datetime.now()
formatted_time = end_time.strftime("End time: %H:%M:%S")
with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
    time_file.write("Finished creating threat profile...\n")
    time_file.write(f"{formatted_time}\n")
    time_file.close()
