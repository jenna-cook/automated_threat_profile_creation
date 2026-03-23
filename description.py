# Title: description.py
# Author: Jenna Cook
# Description: Uses Gemini to produce a description
# of the cybercriminal organization.
# Input: Set the CYBERCRIMINAL_ORG and GENAI_API_KEY
# environment variables.
# Output: A description of the cybercriminal organization in the
# file {CYBERCRIMINAL_ORG}_threat_profile.md where CYBERCRIMINAL_ORG
# is the name of the organization the victims were attacked by.
# This file should be in a directory that is named after the
# cybercriminal organization.

from google import genai
from google.genai.errors import ServerError
import time
import os
from datetime import datetime

# Uses Gemini to produce a description of the cybercriminal organization
def describe_org():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    genai_api_key = os.getenv("GENAI_API_KEY")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Describing...\n")
        time_file.write(f"{formatted_time}\n")
    client = genai.Client(api_key=genai_api_key)
    
    for attempts in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview", contents= f"Give me a description of the cybercriminal group {cybercriminal_org}."
            )
        except ServerError as e:
            # Sleep, then try again if an error is encounter
            print(f"Error {e} - Sleeping for {2 ** attempts} seconds")
            time.sleep(2 ** attempts)
        else:
            break
    
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_threat_profile.md", "a") as f:
        print(response.text)
        f.write(response.text)
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
    describe_org()
