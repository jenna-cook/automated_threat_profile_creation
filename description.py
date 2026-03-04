from google import genai
from google.genai.errors import ServerError
import os
import time
from datetime import datetime

def describe_org():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    genai_api_key = os.getenv("GENAI_API_KEY")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Describing...\n")
        time_file.write(f"{formatted_time}\n")
    client = genai.Client(api_key=genai_api_key)
    
    for attempts in range(6):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview", contents= f"Give me a description of the cybercriminal group {cybercriminal_org}."
            )
        except ServerError as e:
            print(e.code)
            print(attempts)
            if e.code == 503 and attempts < 5:
                print(f"sleep for {2 ** attempts}")
                time.sleep(2 ** attempts)
        else:
            break

    with open(f"./{cybercriminal_org}/{cybercriminal_org}_threat_profile.md", "a") as f:
        f.write(response.text)
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")
