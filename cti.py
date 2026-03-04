from pycti import OpenCTIApiClient
import os
import urllib3
from datetime import datetime
import pytz
import pandas as pd
from tabulate import tabulate


def get_cti():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    opencti_api_key = os.getenv("OPENCTI_API_KEY")
    opencti_instance = os.getenv("OPENCTI_INSTANCE")
    opencti_api_client = OpenCTIApiClient(opencti_instance, opencti_api_key)
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write("Aggregating CTI...\n")
        time_file.write(f"{formatted_time}\n")
    pd.set_option('display.max_rows', None)
    intrusion_set = opencti_api_client.intrusion_set.read(
        filters={
            "mode": "and",
            "filters": [{"key": "name", "values": [cybercriminal_org]}],
            "filterGroups": [],
        }
    )

    stix_relations1 = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Malware"]
    )
    all_relations = []
    after = None

    count = opencti_api_client.stix_core_relationship.list(
        fromTypes=["Indicator"], toId=intrusion_set["id"], first=1, withPagination=True
    )["pagination"]["globalCount"]
    stix_relations2 = opencti_api_client.stix_core_relationship.list(
        fromTypes=["Indicator"], toId=intrusion_set["id"], first=count
    )
    print(f"Count: {count}")
    stix_relations3 = opencti_api_client.stix_core_relationship.list(
        fromId=intrusion_set["id"], toTypes=["Attack-Pattern"], first=200
    )

    with open(f"./{cybercriminal_org}/cti_info.txt", "w") as f:
        with open(f"./{cybercriminal_org}/{cybercriminal_org}_threat_profile.md", "a") as f2:
            f.write("Malware:\n")
            malware= {
                "Name": []
            }
            for stix_relation1 in stix_relations1:
                f.write(f"{stix_relation1["to"]["name"]}\n")
                malware["Name"].append(stix_relation1["to"]["name"])
            df = pd.DataFrame(malware)
            print(df.to_markdown(tablefmt="pipe"))
            f2.write("\n## Malware\n")
            f2.write(df.to_markdown(tablefmt="pipe"))

            f.write("\nIndicators:\n")
            indicators = {
                "Type": [],
                "Name": []
            }
            print(f"stix_relations2 length: {len(stix_relations2)}")
            valid_indicators = {}
            for stix_relation2 in stix_relations2:
                indicator = opencti_api_client.indicator.read(id=stix_relation2["from"]["standard_id"])
                valid_until = indicator["valid_until"]
                #if valid_until:
                expire = datetime.fromisoformat(valid_until)
                if datetime.now(pytz.UTC) > expire:
                        continue
                if valid_until not in valid_indicators:
                    valid_indicators[valid_until] = {
                        "Type": [],
                        "Name": []
                    }
                #observable = opencti_api_client.stix_cyber_observable.list(id=stix_relation2["from"]["id"])
                observable = indicator["x_opencti_observable_values"]
                #print(observable)
                if len(observable) != 0:
                    #print(observable)
                    if observable[0]["type"] == "StixFile":
                        #print(observable[0])
                        f.write(f"{observable[0]["hashes"][0]["algorithm"]} - {observable[0]["hashes"][0]["hash"]}\n")
                        valid_indicators[valid_until]["Type"].append(observable[0]["hashes"][0]["algorithm"])
                        valid_indicators[valid_until]["Name"].append(observable[0]["hashes"][0]["hash"])
                    else:
                        print(observable)
                        f.write(f"{observable[0]["type"]} - {observable[0]["value"]}\n")
                        valid_indicators[valid_until]["Type"].append(observable[0]["type"])
                        valid_indicators[valid_until]["Name"].append(observable[0]["value"])
                else:
                    f.write(f"{stix_relation2["from"]["name"]}\n")
                    valid_indicators[valid_until]["Type"].append("-")
                    valid_indicators[valid_until]["Name"].append(observable[0]["value"])
            print(f"Valid until dictionary: {valid_indicators}")
            for key, value in sorted(valid_indicators.items()):
                df = pd.DataFrame(value)
                valid_until_dt = datetime.fromisoformat(key)
                formatted_date = valid_until_dt.strftime("%B %d, %Y %I:%M %p") + " UTC"
                print(f"Indicators Valid Until {formatted_date}")
                print(df.to_markdown(tablefmt="pipe"))
                f2.write(f"\n## Indicators Valid Until {formatted_date}\n")
                f2.write(df.to_markdown(tablefmt="pipe"))
            f.write("\nAttack Pattern:\n")
            attack_patterns = {
                "Name": [],
                "MITRE ID": [],
            }
            for stix_relation3 in stix_relations3:
        #print(stix_relation3)
        #print(stix_relation3["to"]["name"])
                attack_pattern = opencti_api_client.attack_pattern.read(id=stix_relation3["to"]["standard_id"])
        #print(stix_relation3["to"]["name"])
                f.write(f"{stix_relation3["to"]["name"]} - {attack_pattern["x_mitre_id"]}\n")
                f.write(f"Description: {attack_pattern["description"]}\n\n")
                attack_patterns["Name"].append(stix_relation3["to"]["name"])
                attack_patterns["MITRE ID"].append(f"[{attack_pattern["x_mitre_id"]}](https://attack.mitre.org/techniques/{attack_pattern["x_mitre_id"].replace(".", "/")}/)")
                #attack_patterns["Description"].append(attack_pattern["description"])
            df = pd.DataFrame(attack_patterns)
            print(df.to_markdown(tablefmt="pipe"))
            f2.write("\n## Attack Patterns\n")
            f2.write(df.to_markdown(tablefmt="pipe"))
            f2.write("\n## Appendix\n")
            f2.write("\n### Attack Pattern Descriptions\n")
            for stix_relation3 in stix_relations3:
                attack_pattern = opencti_api_client.attack_pattern.read(id=stix_relation3["to"]["standard_id"])
                f2.write(f"\n#### {stix_relation3["to"]["name"]} - [{attack_pattern["x_mitre_id"]}](https://attack.mitre.org/techniques/{attack_pattern["x_mitre_id"].replace(".", "/")}/)\n")
                f2.write(f"\n{attack_pattern["description"]}\n\n")
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open(f"./{cybercriminal_org}/{cybercriminal_org}_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")    

if __name__ == "__main__":
    get_cti()
