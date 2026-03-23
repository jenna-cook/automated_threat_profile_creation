# Title: chart.py
# Author: Jenna Cook
# Description: Creates a bar chart showing the number
# of victims in each NAICS sector.
# Input: Run sorting.py to ensure there is a list of
# categorized victims. Set the CYBERCRIMINAL_ORG
# environment variable.
# Output: A bar chart showing the number of victims in
# each NAICS sector in a file called 
# {CYBERCRIMINAL_ORG}_barchart.png where CYBERCRIMINAL_ORG
# is the name of the organization the victims were attacked by.
# This file should be in a directory that is named after the
# cybercriminal organization.

import matplotlib.pyplot as plt
import re
import numpy as np
import os
from datetime import datetime

# Creates a bar chart showing the number of victims in each NAICS sector
def create_chart():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Generating chart...\n")
        time_file.write(f"{formatted_time}\n")
    # Keeps track of the number of victims in each category
    categories = {"Uncategorized": 0,
                  "Agriculture, Forestry, Fishing and Hunting": 0,
                  "Mining": 0,
                  "Utilities": 0,
                  "Construction": 0,
                  "Manufacturing": 0,
                  "Wholesale Trade": 0,
                  "Retail Trade": 0,
                  "Transportation and Warehousing": 0,
                  "Information": 0,
                  "Finance and Insurance": 0,
                  "Real Estate Rental and Leasing": 0,
                  "Professional, Scientific, and Technical Services": 0,
                  "Management of Companies and Enterprises": 0,
                  "Administrative and Support and Waste Management and Remediation Services": 0,
                  "Educational Services": 0,
                  "Health Care and Social Assistance": 0,
                  "Arts, Entertainment, and Recreation": 0,
                  "Accommodation and Food Services": 0,
                  "Other Services (except Public Administration)": 0, 
                  "Public Administration": 0}

    with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt") as f:
        for victim in f:
            name, category = victim.strip().split(": ")
            categories[category] = categories[category] + 1
    
    # Remove the empty categories, so they aren't included in the final chart
    filtered_categories = {key: value for key, value in categories.items() if value != 0}
    # Put the categories in order from the category with the least victims to
    # the one with the most
    sorted_categories = dict(sorted(filtered_categories.items(), key=lambda item: item[1]))
    print(sorted_categories)
    sizes = [value for value in sorted_categories.values()]
    print(sizes)
    labels = []
    
    # Add the categories to the label
    for category, victim in sorted_categories.items():
        if category == "Administrative and Support and Waste Management and Remediation Services":
            labels.append("Administrative and Support and Waste\nManagement and Remediation Services")
        else:
            labels.append(category)
    # Put the NAICS sectors on the x-axis
    x = np.array(labels)
    # Put the number of victims on the y-axis
    y = np.array(sizes)
    plt.figure(figsize=(10, 7))
    # Make the bar chart horizontal
    plt.barh(x, y)

    # Include the number of victims next to each bar
    for i in range(len(sizes)):
        plt.text(sizes[i]+0.5, i, sizes[i], va="center")
    plt.title(f"{cybercriminal_org} Victims Categorized by NAICS")
    # Since the barchart is horizontal, the "Number of Victims" label goes on the x-axis
    plt.xlabel("Number of Victims")
    # Since the barchart is horizontal, the "NAICS Sectors" label goes on the y-axis
    plt.ylabel("NAICS Sectors")
    # Add lines, so it is easier to read the bar chart
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"./{cybercriminal_org}/{cybercriminal_org}_barchart.png", transparent=True)
    # Track the end time, so the amount of time the function runs can be calculated
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")
if __name__ == "__main__":
    # The code below allows the script to be run on its own
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    dir_path = f"./{cybercriminal_org}"
    os.makedirs(dir_path, exist_ok=True)
    create_chart()
