from google import genai
from google.genai.errors import ServerError
from datetime import datetime, timedelta
from pathlib import Path
import time
import re
import logging
logging.getLogger().setLevel(logging.ERROR)
import os

def sort():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    genai_api_key = os.getenv("GENAI_API_KEY")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Sorting...\n")
        time_file.write(f"{formatted_time}\n")

    category_number_to_name = {'-1': "Revision", '0': "Uncategorized", '11': "Agriculture, Forestry, Fishing and Hunting", '21': "Mining", '22': "Utilities", '23': "Construction", '31-33': "Manufacturing", '42': "Wholesale Trade", '44-45': "Retail Trade", '48-49': "Transportation and Warehousing", '51': "Information", '52': "Finance and Insurance",'53': "Real Estate Rental and Leasing", '54': "Professional, Scientific, and Technical Services", '55': "Management of Companies and Enterprises", '56': "Administrative and Support and Waste Management and Remediation Services", '61': "Educational Services", '62': "Health Care and Social Assistance", '71': "Arts, Entertainment, and Recreation", '72': "Accommodation and Food Services", '81': "Other Services (except Public Administration)", '92': "Public Administration"}

    client = genai.Client(api_key=genai_api_key)

    #for x in range(10):
    victims_sorted = {}
    path = Path(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt")
    if path.exists() and path.stat().st_size > 0:
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "r") as f0:
            for x in f0:
                name, category = x.strip().split(": ")
                victims_sorted[name] = category
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims.txt", "r") as f:
        i = 0
        prompt=""
        current_time = datetime.now()
        formatted_time = current_time.strftime("Current time: %H:%M:%S")
        future_time = current_time + timedelta(minutes=1)
        with open(f"./{cybercriminal_org}/gemini_response.txt", "a") as f1:
            f1.write(f"{formatted_time}\n")
            for x in f:
                current_time = datetime.now()
                formatted_time = current_time.strftime("Current time: %H:%M:%S")
                formatted_time2 = future_time.strftime("Future time: %H:%M:%S")
                name_and_link = x.strip().split(": ")
                name = name_and_link[0]
                if name in victims_sorted:
                    continue
                if len(name_and_link) > 1:
                    link = name_and_link[1]
                    prompt = f"Give me the NAICS code for {name} ({link}) in the format “NAICS: #” and explain your reasoning in one sentence."
                else:
                    prompt =  f"Give me the NAICS code for {name} in the format “NAICS: #” and explain your reasoning in one sentence."
                if i < 999 and current_time < future_time:
                    for attempts in range(6):
                        try:
                            response = client.models.generate_content(
                                model="gemini-3-flash-preview", contents=prompt
                            )
                        except ServerError as e:
                            print(e.code)
                            print(attempts)
                            if attempts < 5:
                                print(f"sleep for {2 ** attempts}")
                                time.sleep(2 ** attempts)
                            else:
                                print("skip sleep")
                                with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "a") as f2:
                                    for victim_name, victim_category in victims_sorted.items():
                                        f2.write(f"{victim_name}: {victim_category}\n")
                                raise
                        else:
                            break
                    print("Prompt: ")
                    print(prompt)
                    print("Response: ")
                    print(response.text)
                    i += 1
                    #time.sleep(1)
                else:
                    while current_time < future_time:
                        time.sleep(1)
                        current_time = datetime.now()
                    time.sleep(1)
                    current_time = datetime.now()
                    future_time = current_time + timedelta(minutes=1)
                    for attempts in range(6):
                        try:
                            response = client.models.generate_content(
                                model="gemini-3-flash-preview", contents=prompt
                            )
                        except ServerError as e:
                            print(e.code)
                            print(attempts)
                            if attempts < 5:
                                print(f"sleep for {2 ** attempts}")
                                time.sleep(2 ** attempts)
                            else:
                                print("skip sleep 2")
                                with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "a") as f2:
                                    for victim_name, victim_category in victims_sorted.items():
                                        f2.write(f"{victim_name}: {victim_category}\n")
                                raise
                        else:
                            break
                    i = 1
                    #print(response.text)
                    #with open("victims_sorted.txt2.txt", "a") as f2:
                f1.write(f"{response.text}\n")
                if response.text is None:
                    print("Re-prompt attempt in progress...")
                    for attempts in range(6):
                        try:
                            response = client.models.generate_content(
                                model="gemini-3-flash-preview", contents=prompt
                        )
                        except ServerError as e:
                            print(e.code)
                            print(attempts)
                            if attempts < 5:
                                print(f"sleep for {2 ** attempts}")
                                time.sleep(2 ** attempts)
                            else:
                                print("skip sleep")
                                with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "a") as f2:
                                    for victim_name, victim_category in victims_sorted.items():
                                        f2.write(f"{victim_name}: {victim_category}\n")
                                raise
                        else:
                            break
                    print("Prompt: ")
                    print(prompt)
                    print("Response: ")
                    print(response.text)
                    i += 1
                else:
                    match = re.search(r"NAICS: (\d+)", response.text)
                    if match:
                        category_number = match.group(1)[:2]
                        if category_number == '31' or category_number == '32' or category_number == '33':
                            category_number = '31-33'
                        elif category_number == '44' or category_number == '45':
                            category_number = '44-45'
                        elif category_number == '48' or category_number == '49':
                            category_number = '48-49'
                        if category_number not in category_number_to_name:
                            print("Re-prompt attempt in progress...")
                            for attempts in range(6):
                                try:
                                    response = client.models.generate_content(
                                        model="gemini-3-flash-preview", contents=prompt
                                   )
                                except ServerError as e:
                                    print(e.code)
                                    print(attempts)
                                    if attempts < 5:
                                        print(f"sleep for {2 ** attempts}")
                                        time.sleep(2 ** attempts)
                                    else:
                                        print("skip sleep")
                                        with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "a") as f2:
                                            for victim_name, victim_category in victims_sorted.items():
                                                f2.write(f"{victim_name}: {victim_category}\n")
                                        raise
                                else:
                                    break
                            print("Prompt: ")
                            print(prompt)
                            print("Response: ")
                            print(response.text)
                            i += 1
                    else:
                        print("Re-prompt attempt in progress...")
                        for attempts in range(6):
                            try:
                                response = client.models.generate_content(
                                    model="gemini-3-flash-preview", contents=prompt
                                )
                            except ServerError as e:
                                print(e.code)
                                print(attempts)
                                if attempts < 5:
                                    print(f"sleep for {2 ** attempts}")
                                    time.sleep(2 ** attempts)
                                else:
                                    print("skip sleep")
                                    with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "a") as f2:
                                        for victim_name, victim_category in victims_sorted.items():
                                            f2.write(f"{victim_name}: {victim_category}\n")
                                    raise
                            else:
                                break
                        print("Prompt: ")
                        print(prompt)
                        print("Response: ")
                        print(response.text)
                        i += 1
                if response.text is not None:
                    match = re.search(r"NAICS: (\d+)", response.text)
                    if match:
                        category_number = match.group(1)[:2]
                        if category_number == '31' or category_number == '32' or category_number == '33':
                            category_number = '31-33'
                        elif category_number == '44' or category_number == '45':
                            category_number = '44-45'
                        elif category_number == '48' or category_number == '49':
                            category_number = '48-49'
                        if category_number in category_number_to_name:
                            victims_sorted[name] = category_number_to_name[category_number]
                            print(f"{name}: {category_number_to_name[category_number]}")
                        else:
                            victims_sorted[name] = "Uncategorized"
                            print(f"{name}: Uncategorized")
                    else:
                        victims_sorted[name] = "Uncategorized"
                        print(f"{name}: Uncategorized")
                else:
                    victims_sorted[name] = "Uncategorized"
                    print(f"{name}: Uncategorized")
            current_time = datetime.now()
            formatted_time = current_time.strftime("Current time: %H:%M:%S")
            f1.write(f"{formatted_time}\n")
        y_or_n = "y"
        while y_or_n == "y":
            current_time = datetime.now()
            formatted_time = current_time.strftime("Current time: %H:%M:%S")
            with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
                time_file.write("Prompt user...\n")
                time_file.write(f"{formatted_time}\n")
            y_or_n = input("Would you like to edit a victim's category? (y/n) ")
            if y_or_n == "y":
                victim_name = input("Which victim do you want to edit? ")
                victim_category = input(f"What is {victim_name}'s updated category? ")
                victims_sorted[victim_name] = victim_category
                print(f"{victim_name}: {victim_category}")
        
        current_time = datetime.now()
        formatted_time = current_time.strftime("Current time: %H:%M:%S")
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
            time_file.write("User response given...\n")
            time_file.write(f"{formatted_time}\n")
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "w") as f2:
            for victim_name, victim_category in victims_sorted.items():
                f2.write(f"{victim_name}: {victim_category}\n")
        end_time = datetime.now()
        formatted_time = end_time.strftime("End time: %H:%M:%S")
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
            time_file.write(f"{formatted_time}\n")

if __name__ == "__main__":
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    dir_path = f"./{cybercriminal_org}"
    sort()
