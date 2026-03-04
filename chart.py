import matplotlib.pyplot as plt
import re
import numpy as np
import os
from datetime import datetime
#categories = {'0': 0, '11': 0, '21': 0, '22': 0, '23': 0, '31-33': 0, '42': 0, '44-45': 0, '48-49': 0, '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '61': 0, '62': 0, '71': 0, '72': 0, '81': 0, '92': 0}

def create_chart():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Generating chart...\n")
        time_file.write(f"{formatted_time}\n")
    categories = {"Uncategorized": 0, "Agriculture, Forestry, Fishing and Hunting": 0, "Mining": 0, "Utilities": 0, "Construction": 0, "Manufacturing": 0, "Wholesale Trade": 0, "Retail Trade": 0, "Transportation and Warehousing": 0, "Information": 0, "Finance and Insurance": 0, "Real Estate Rental and Leasing": 0, "Professional, Scientific, and Technical Services": 0, "Management of Companies and Enterprises": 0, "Administrative and Support and Waste Management and Remediation Services": 0, "Educational Services": 0, "Health Care and Social Assistance": 0, "Arts, Entertainment, and Recreation": 0, "Accommodation and Food Services": 0, "Other Services (except Public Administration)": 0, "Public Administration": 0}
    i=0
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt") as f:
        for x in f:
            name, category = x.strip().split(": ")
            categories[category] = categories[category] + 1
            i = i + 1

    filtered_categories = {key: value for key, value in categories.items() if value != 0}
    sorted_categories = dict(sorted(filtered_categories.items(), key=lambda item: item[1]))
    print(sorted_categories)
    sizes = [value for value in sorted_categories.values()]
    print(sizes)
    labels = []

    for key, value in sorted_categories.items():
        if key == "Administrative and Support and Waste Management and Remediation Services":
            labels.append("Administrative and Support and Waste\nManagement and Remediation Services")
        else:
            labels.append(key)
    x = np.array(labels)
    y = np.array(sizes)
    plt.figure(figsize=(10, 7))
    plt.barh(x, y)
    for i in range(len(sizes)):
        plt.text(sizes[i]+0.5, i, sizes[i], va="center")
    plt.title(f"{cybercriminal_org} Victims Categorized by NAICS")
    plt.xlabel("Number of Victims")
    plt.ylabel("NAICS Sectors")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"./{cybercriminal_org}/{cybercriminal_org}_barchart.png", transparent=True)
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")
if __name__ == "__main__":
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    dir_path = f"./{cybercriminal_org}"
    create_chart()
