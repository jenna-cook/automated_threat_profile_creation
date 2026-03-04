import os
import scrape
import description
import cti
import sorting
import chart
from datetime import datetime

start_time = datetime.now()
formatted_date = start_time.strftime("%B %d, %Y")
formatted_time = start_time.strftime("Start time: %H:%M:%S")
cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
scraping_func = os.getenv("SCRAPING_FUNC")
dir_path = f"./{cybercriminal_org}"
os.makedirs(dir_path, exist_ok=True)
with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "w") as time_file:
    time_file.write("Start creating threat profile...\n")
    time_file.write(f"{formatted_time}\n")
    time_file.close()

scraping = getattr(scrape, scraping_func)
scraping()
sorting.sort()
chart.create_chart()
with open(f"{dir_path}/{cybercriminal_org}_threat_profile.md", "w") as f:
    f.write(f"# {cybercriminal_org} Threat Profile\n")
    f.write(f"### Date: {formatted_date}\n\n")
    f.close()
description.describe_org()
with open(f"{dir_path}/{cybercriminal_org}_threat_profile.md", "a") as f:
    chart_path = f"./{cybercriminal_org}_barchart.png"
    chart_path_url_encoded_space = chart_path.replace(" ", "%20")
    f.write(f'\n\n## Industry Targeting !["{cybercriminal_org} Victims Categorized By NAICS"]("{chart_path_url_encoded_space}")\n')
    f.close()
cti.get_cti()
end_time = datetime.now()
formatted_time = end_time.strftime("End time: %H:%M:%S")
with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
    time_file.write("Finished creating threat profile...\n")
    time_file.write(f"{formatted_time}\n")
    time_file.close()
