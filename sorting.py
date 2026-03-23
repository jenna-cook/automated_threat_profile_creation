# Title: sorting.py
# Author: Jenna Cook
# Description: Uses Gemini to categorize
# vitims by NAICS sector.
# Input: Run scrape.py to ensure there is a list of
# victims to categorize. Set the CYBERCRIMINAL_ORG 
# and GENAI_API_KEY environment variables.
# Output: A list of victims and their NAICS sectors
# in a file called {CYBERCRIMINAL_ORG}_victims_sorted.txt
# where CYBERCRIMINAL_ORG is the name of the organization
# the victims were attacked by. Gemini's responses are 
# saved in gemini_response.txt for verification. These files
# should be in a directory that is named after the
# cybercriminal organization.

from google import genai
from google.genai.errors import ServerError
from datetime import datetime, timedelta
from pathlib import Path
import time
import re
import logging
# The output is difficult to read if the 
# logging isn't this level
logging.getLogger().setLevel(logging.ERROR)
import os

# Prompts Gemini and reattempts the prompt
# if there was a server error. If there was 
# an error, then the victims already sorted
# get saved.
def prompt_gemini(client, prompt, victims_sorted):
    for attempts in range(6):
        try:
            # The model can be changed to other Gemini models
            response = client.models.generate_content(
                    model="gemini-3-flash-preview", contents=prompt
            )
        except ServerError as e:
            if attempts < 5:
                # Sleep, then try again if an error is encounter
                print(f"Error {e} - Sleeping for {2 ** attempts} seconds")
                time.sleep(2 ** attempts)
            else:
                # After five attempts, save the victims already sorted before the program exits
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
    return response

# Categorizes victims into NAICS sectors using Gemini
def sort():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    genai_api_key = os.getenv("GENAI_API_KEY")
    # Track the start time, so the amount of time the function runs can be calculated
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Sorting...\n")
        time_file.write(f"{formatted_time}\n")

    # This dictionary makes it easy to get the sector name from the first two digits of an NAICS code
    category_number_to_name = {'0': "Uncategorized",
                               '11': "Agriculture, Forestry, Fishing and Hunting",
                               '21': "Mining",
                               '22': "Utilities",
                               '23': "Construction",
                               '31-33': "Manufacturing",
                               '42': "Wholesale Trade",
                               '44-45': "Retail Trade",
                               '48-49': "Transportation and Warehousing",
                               '51': "Information",
                               '52': "Finance and Insurance",
                               '53': "Real Estate Rental and Leasing",
                               '54': "Professional, Scientific, and Technical Services",
                               '55': "Management of Companies and Enterprises",
                               '56': "Administrative and Support and Waste Management and Remediation Services",
                               '61': "Educational Services",
                               '62': "Health Care and Social Assistance",
                               '71': "Arts, Entertainment, and Recreation",
                               '72': "Accommodation and Food Services",
                               '81': "Other Services (except Public Administration)",
                               '92': "Public Administration"}

    client = genai.Client(api_key=genai_api_key)

    victims_sorted = {}
    path = Path(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt")
    # If this file exists and is not empty, then some victims have already been categorized
    if path.exists() and path.stat().st_size > 0:
        # If there are victims that have been sorted before, put them in victims_sorted,
        # so they don't get categorized again
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "r") as sorted_victims:
            for sorted_victim in sorted_victims:
                name, category = sorted_victim.strip().split(": ")
                victims_sorted[name] = category

    # Get the list of victims
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims.txt", "r") as f:
        i = 0
        prompt=""
        response=""
        current_time = datetime.now()
        formatted_time = current_time.strftime("Current time: %H:%M:%S")
        # Since there is a limit to how many prompts can be sent per minute
        # we need to know at what time the prompts per minute is reset
        future_time = current_time + timedelta(minutes=1)
        # Keep track of Gemini's responses, so they can be verified by the user
        with open(f"./{cybercriminal_org}/gemini_response.txt", "a") as f1:
            for victims in f:
                current_time = datetime.now()
                # Get the victim's information
                name_and_link = victims.strip().split(": ")
                name = name_and_link[0]
                # If the victim has already been sorted, then we don't need to
                # do it again
                if name in victims_sorted:
                    continue
                # Check to see if there is a link with the name
                if len(name_and_link) > 1:
                    link = name_and_link[1]
                    # If there is a link to the victim's website, add it to the prompt
                    prompt = f"Give me the NAICS code for {name} ({link}) in the format “NAICS: #” and explain your reasoning in one sentence."
                else:
                    # Not every DLS provides a link to the victim's website
                    prompt =  f"Give me the NAICS code for {name} in the format “NAICS: #” and explain your reasoning in one sentence."
                # Check to make sure that the number of prompts hasn't exceeded the
                # limit of prompts per minute. Each model has a limit on prompts per
                # minute, so make sure the limit of prompts per minute in the if statement
                # below matches the one associated with the model responding to the prompts. 
                if i < 999 and current_time < future_time:
                    response = prompt_gemini(client, prompt, victims_sorted)
                    # Increase by one since a prompt was sent to Gemini
                    i += 1
                # If the number of prompts that has been sent is at the limit of prompts
                # per minute, then wait until the minute has passed before continuing.
                else:
                    # Sleep until the minute has passed
                    while current_time < future_time:
                        time.sleep(1)
                        current_time = datetime.now()
                    time.sleep(1)
                    current_time = datetime.now()
                    future_time = current_time + timedelta(minutes=1)
                    # Now that the number of prompts sent has been reset because a minute
                    # has passed, prompts can be sent again to Gemini
                    response = prompt_gemini(client, prompt, victims_sorted)
                    i = 1
                f1.write(f"{response.text}\n")
                # Sometimes Gemini responds with None, so the prompt is
                # sent again in this scenario
                if response.text is None:
                    print("Reprompt attempt in progress...")
                    response = prompt_gemini(client, prompt, victims_sorted)
                    i += 1
                # Sometimes Gemini may respond, but it may not
                # be in the correct format or the number it provides may
                # not be associated with an NAICS sector, so the prompt
                # is sent again
                if response.text is not None:
                    match = re.search(r"NAICS: (\d+)", response.text)
                    # The response has the code in the "NAICS: #" format
                    if match:
                        category_number = match.group(1)[:2]
                        if category_number == '31' or category_number == '32' or category_number == '33':
                            category_number = '31-33'
                        elif category_number == '44' or category_number == '45':
                            category_number = '44-45'
                        elif category_number == '48' or category_number == '49':
                            category_number = '48-49'
                        # If there is no NAICS sector associated with the code
                        # Gemini provided, then Gemini is sent the prompt again
                        if category_number not in category_number_to_name:
                            print("Reprompt attempt in progress...")
                            response = prompt_gemini(client, prompt, victims_sorted)
                            i += 1
                    # If Gemini's response is not in the "NAICS: #" format, the
                    # prompt is sent again
                    else:
                        print("Reprompt attempt in progress...")
                        response = prompt_gemini(client, prompt, victims_sorted)
                        i += 1
                # If after reprompting Gemini there are still invalid responses,
                # the victim gets put into the "Uncategorized" category
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
                        # If there is a NAICS sector associated with the code
                        # Gemini provided, add the victim and sector to
                        # victims_sorted.
                        if category_number in category_number_to_name:
                            victims_sorted[name] = category_number_to_name[category_number]
                            print(f"{name}: {category_number_to_name[category_number]}")
                        # If there is no NAICS sector associated with the code
                        # Gemini provided, label the victim "Uncategorized"
                        else:
                            victims_sorted[name] = "Uncategorized"
                            print(f"{name}: Uncategorized")
                    # If Gemini's response is not in the "NAICS: #"
                    # format, label the victim "Uncategorized"
                    else:
                        victims_sorted[name] = "Uncategorized"
                        print(f"{name}: Uncategorized")
                # If the response from Gemini is None, label the
                # victim "Uncategorized"
                else:
                    victims_sorted[name] = "Uncategorized"
                    print(f"{name}: Uncategorized")

        y_or_n = "y"
        while y_or_n == "y":
            # Track the time of when user input is requested, so it isn't included in
            # the amount of time the function takes to run
            current_time = datetime.now()
            formatted_time = current_time.strftime("Current time: %H:%M:%S")
            with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
                time_file.write("Prompt user...\n")
                time_file.write(f"{formatted_time}\n")
            # Ask the user if there is a victim's category they want to change. This is the user's
            # opportunity to correct any mistakes Gemini may have made.
            y_or_n = input("Would you like to edit a victim's category? (y/n) ")
            if y_or_n == "y":
                victim_name = input("Which victim do you want to edit? ")
                victim_category = input(f"What is {victim_name}'s updated category? ")
                victims_sorted[victim_name] = victim_category
                print(f"{victim_name}: {victim_category}")
        # Track the time of when user input is finished, so it isn't included in
        # the amount of time the function takes to run
        current_time = datetime.now()
        formatted_time = current_time.strftime("Current time: %H:%M:%S")
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
            time_file.write("User response given...\n")
            time_file.write(f"{formatted_time}\n")
        # Save all the victims and their categories in a file
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_victims_sorted.txt", "w") as f2:
            for victim_name, victim_category in victims_sorted.items():
                f2.write(f"{victim_name}: {victim_category}\n")
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
    sort()
