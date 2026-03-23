# Title: cti.py
# Author: Jenna Cook
# Description: Uses OpenCTI to aggregate information
# on malware, indicators, and attack patterns 
# associated with a cybercriminal organization. 
# Input: Set the CYBERCRIMINAL_ORG, OPENCTI_API_KEY, and
# OPENCTI_INSTANCE environment variables.
# Output: Tables of malware, indicators, and attack patterns in
# addition to attack pattern descriptions are included in a file
# called {CYBERCRIMINAL_ORG}_threat_profile.md where CYBERCRIMINAL_ORG is the
# name of the cybercriminal organization the Cyber Threat Intelligience (CTI)
# is associated with. The CTI is also included in the file cti_info.txt.
# These files should be in a directory that is named after the
# cybercriminal organization.

from pycti import OpenCTIApiClient
import os
from datetime import datetime
import pytz
import pandas as pd

# Uses OpenCTI to aggregate information on malware, indicators, and attack patterns
# associated with a cybercriminal organizations
def get_cti():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    opencti_api_key = os.getenv("OPENCTI_API_KEY")
    opencti_instance = os.getenv("OPENCTI_INSTANCE")
    opencti_api_client = OpenCTIApiClient(opencti_instance, opencti_api_key)
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Aggregating CTI...\n")
        time_file.write(f"{formatted_time}\n")
    
    # Get information related to the cybercriminal organization
    intrusion_set = opencti_api_client.intrusion_set.read(
        filters={
            "mode": "and",
            "filters": [{"key": "name", "values": [cybercriminal_org]}],
            "filterGroups": [],
        }
    )
    
    # Get the number of malware
    malware_count = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Malware"], first=1, withPagination=True
    )["pagination"]["globalCount"]
    # Get the information on malware associated with the cybercriminal organization
    stix_relations_malware = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Malware"], first=malware_count
    )
    
    # Get the number of indicators
    indicator_count = opencti_api_client.stix_core_relationship.list(
        fromTypes=["Indicator"], toId=intrusion_set["id"], first=1, withPagination=True
    )["pagination"]["globalCount"]
    # Get the information on indicators associated with the cybercriminal organization
    stix_relations_indicator = opencti_api_client.stix_core_relationship.list(
        fromTypes=["Indicator"], toId=intrusion_set["id"], first=indicator_count
    )
    # Get the number of attack patterns
    ap_count = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Attack-Pattern"], first=1, withPagination=True
    )["pagination"]["globalCount"]
    # Get the information on attack patterns associated with the cybercriminal organization
    stix_relations_ap = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Attack-Pattern"], first=ap_count
    )

    with open(f"./{cybercriminal_org}/cti_info.txt", "w") as f:
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_threat_profile.md", "a") as tp:
            f.write("Malware:\n")
            # Store the names of malware
            malware= {
                "Name": []
            }
            # Get the names of the malware
            for stix_relation_malware in stix_relations_malware:
                f.write(f"{stix_relation_malware["to"]["name"]}\n")
                malware["Name"].append(stix_relation_malware["to"]["name"])
            # Put the malware names into a table
            df = pd.DataFrame(malware)
            print(df.to_markdown(tablefmt="pipe"))
            tp.write("\n## Malware\n")
            # Put that table into the threat profile in markdown
            tp.write(df.to_markdown(tablefmt="pipe"))

            f.write("\nIndicators:\n")
            # Store the type and name of indicators
            indicators = {
                "Type": [],
                "Name": []
            }
            # Not all indicators are valid, since some indicators are past their
            # expiration date. For this reason we keep track of the valid indicators
            # specifically.
            valid_indicators = {}
            # Get valid indicators
            for stix_relation_indicator in stix_relations_indicator:
                indicator = opencti_api_client.indicator.read(id=stix_relation_indicator["from"]["standard_id"])
                valid_until = indicator["valid_until"]
                expire = datetime.fromisoformat(valid_until)
                # If the indicator has expired, don't include it in the threat profile
                if datetime.now(pytz.UTC) > expire:
                        continue
                # The indicators are grouped by the date they are valid until.
                # If there isn't a grouping of indicators for a valid until date
                # then create a new grouping with this date.
                if valid_until not in valid_indicators:
                    valid_indicators[valid_until] = {
                        "Type": [],
                        "Name": []
                    }
                observable = indicator["x_opencti_observable_values"]
                # If observable is not empty, then there is a type for the indicator
                if len(observable) != 0:
                    # If the type is a stixFile, make the type the hash algorithm instead
                    if observable[0]["type"] == "StixFile":
                        f.write(f"{observable[0]["hashes"][0]["algorithm"]} - {observable[0]["hashes"][0]["hash"]}\n")
                        valid_indicators[valid_until]["Type"].append(observable[0]["hashes"][0]["algorithm"])
                        valid_indicators[valid_until]["Name"].append(observable[0]["hashes"][0]["hash"])
                    else:
                        f.write(f"{observable[0]["type"]} - {observable[0]["value"]}\n")
                        valid_indicators[valid_until]["Type"].append(observable[0]["type"])
                        valid_indicators[valid_until]["Name"].append(observable[0]["value"])
                # If there is no type, then put "-" as the type to indicate there is no type for
                # this indicator
                else:
                    f.write(f"{stix_relation_indicator["from"]["name"]}\n")
                    valid_indicators[valid_until]["Type"].append("-")
                    valid_indicators[valid_until]["Name"].append(stix_relation_indicator["from"]["name"])
            # Sort the dates of the valid indicators into ascending order
            for date, indicators in sorted(valid_indicators.items()):
                # Put the valid indicators in a table
                df = pd.DataFrame(indicators)
                valid_until_dt = datetime.fromisoformat(date)
                formatted_date = valid_until_dt.strftime("%B %d, %Y %I:%M %p") + " UTC"
                print(f"Indicators Valid Until {formatted_date}")
                print(df.to_markdown(tablefmt="pipe"))
                tp.write(f"\n## Indicators Valid Until {formatted_date}\n")
                # Put that table into the threat profile in markdown
                tp.write(df.to_markdown(tablefmt="pipe"))
            
            f.write("\nAttack Pattern:\n")
            # Store the name and MITRE ID of the attack patterns
            attack_patterns = {
                "Name": [],
                "MITRE ID": [],
            }
            # Get the name and MITRE ID of the attack patterns
            for stix_relation_ap in stix_relations_ap:
                attack_pattern = opencti_api_client.attack_pattern.read(id=stix_relation_ap["to"]["standard_id"])
                f.write(f"{stix_relation_ap["to"]["name"]} - {attack_pattern["x_mitre_id"]}\n")
                f.write(f"Description: {attack_pattern["description"]}\n\n")
                attack_patterns["Name"].append(stix_relation_ap["to"]["name"])
                # MITRE has a website with links about each attack pattern, so the link is attached to the ID
                mitre_link = f"https://attack.mitre.org/techniques/{attack_pattern["x_mitre_id"].replace(".", "/")}/"
                attack_patterns["MITRE ID"].append(f"[{attack_pattern["x_mitre_id"]}]({mitre_link})")
            # Put the attack patterns in a table
            df = pd.DataFrame(attack_patterns)
            print(df.to_markdown(tablefmt="pipe"))
            tp.write("\n## Attack Patterns\n")
            # Put that table into the threat profile in markdown
            tp.write(df.to_markdown(tablefmt="pipe"))
            tp.write("\n## Appendix\n")
            tp.write("\n### Attack Pattern Descriptions\n")
            # Since the descriptions of the attack patterns can be long
            # it is included in the appendix of the threat profile
            for stix_relation_ap in stix_relations_ap:
                attack_pattern = opencti_api_client.attack_pattern.read(id=stix_relation_ap["to"]["standard_id"])
                mitre_link = f"https://attack.mitre.org/techniques/{attack_pattern["x_mitre_id"].replace(".", "/")}/"
                tp.write(f"\n#### {stix_relation_ap["to"]["name"]} - [{attack_pattern["x_mitre_id"]}]({mitre_link})\n")
                tp.write(f"\n{attack_pattern["description"]}\n\n")
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
    get_cti()
