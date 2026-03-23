# Title: scrape.py
# Author: Jenna Cook
# Description: Creates a list of victims
# by scraping a Dedicated Leak Site (DLS). Currently
# there are only three functions that scrape
# dedicated leak sites. Additional functions
# will need to be created to scrape new
# dedicated leak sites.
# Input: Set the CYBERCRIMINAL_ORG and
# SCRAPE_FUNC environment variables.
# Output: A list of victims in a file called
# {CYBERCRIMINAL_ORG}_victims.txt where
# CYBERCRIMINAL_ORG is the name of the organization
# the victims were attacked by. The file should
# be in a directory that is named after the
# cybercriminal organization.

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError, Error
import time
import os
from datetime import datetime

# Scrapes the Rhysida dedicated leak site and produces a list of victims from it
def scrape_rhysida():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./Rhysida/Rhysida_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")

    # The onion link of the DLS can't be accessed unless Tor is used
    tor_proxy = "socks5://127.0.0.1:9050"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )

        page = browser.new_page()
        for i in range(5):
            try:
                # All the victims are on one page
                page.goto("http://rhysidafohrhyy2aszi7bm32tnjat5xri65fopcxkdfxhi4tidsg7cad.onion/archive.php", wait_until="domcontentloaded")
            except (TimeoutError, Error) as e:
                # Sleep, then try again if an error is encounter
                print(f"Error {e} - Sleepig for {2 ** i} seconds")
                time.sleep(2 ** i)
            else:
                break
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        # Parse the HTML and get the victim names and links
        victims = soup.find_all('div', class_ = 'col-10')
        with open("./Rhysida/Rhysida_victims.txt", "w") as f:
            for victim in victims:
                victim_info = victim.find('div', class_ = 'h4')
                victim_name = victim_info.find('a')
                victim_link = victim_name['href']
                victim_name_text = victim_name.text.strip()
                f.write(f"{victim_name_text}: {victim_link}\n")
                print(f"{victim_name_text}: {victim_link}\n")
        browser.close()
    
    # Track the end time, so the amount of time the function runs can be calculated
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./Rhysida/Rhysida_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")


# Scrapes the Play dedicated leak site and produces a list of victims from it
def scrape_play():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./Play/Play_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")
    
    # The onion link of the DLS can't be accessed unless Tor is used
    tor_proxy = "socks5://127.0.0.1:9050"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )
        with open("./Play/Play_victims.txt", "w") as f:
            page_num = 1
            max_page_num = 1
            # Since the victims span multiple pages, the pages
            # need to be looped through
            while page_num <= max_page_num:
                page = browser.new_page()
                for i in range(5):
                    try:
                        # The pages are indexed by changing the page number in the link
                        page.goto(f'http://k7kg3jqxang3wh7hnmaiokchk7qoebupfgoik6rha6mjpzwupwtj25yd.onion/index.php?page={page_num}',
                                  wait_until="domcontentloaded")
                    except (TimeoutError, Error) as e:
                        # Sleep, then try again if an error is encounter
                        print(f"Error {e} - Sleepig for {2 ** i} seconds")
                        time.sleep(2 ** i)
                    else:
                        break
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                # Get the max page number displayed on the first page. Since
                # page_num and max_page_num both equal one to start, this
                # code will be reached whenever the first page is accessed.
                if page_num == max_page_num:
                    pages = soup.find_all('span', class_='Page')
                    max_page_num = int(pages[len(pages)-1].text.strip())
                    print(f"Max page number: {max_page_num}")
                # Parse the HTML and get the victim names and links
                victims = soup.find_all('th', class_ = 'News')
                for victim in victims:
                    victim_link = victim.find('i', class_='link')
                    victim_link_text = victim_link.next_sibling.text.strip()
                    victim_name_text = victim.find(string=True, recursive=False)
                    f.write(f"{victim_name_text} ({victim_link_text})\n")
                    print(f"{victim_name_text} ({victim_link_text})\n")
                page_num += 1
        browser.close()
    # Track the end time, so the amount of time the function runs can be calculated
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./Play/Play_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")

# Scrapes the INC Ransom dedicated leak site and produces a list of victims from it
def scrape_inc_ransom():
    # Track the start time, so the amount of time the function runs can be calculated
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./INC Ransom/INC Ransom_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")
    
    # The onion link of the DLS can't be accessed unless Tor is used
    tor_proxy = "socks5://127.0.0.1:9050"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )

        page = browser.new_page()
        for i in range(5):
            try:
                page.goto("http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures", wait_until="networkidle")
            except (TimeoutError, Error) as e:
                # Sleep, then try again if an error is encounter
                print(f"Error {e} - Sleepig for {2 ** i} seconds")
                time.sleep(2 ** i)
            else:
                break
        # Not all the victims are shown unless a button on the page is clicked repeatedly 
        while True:
            try:
                button = page.wait_for_selector(".more__container.text-primary.cursor-pointer.p-12.text-sm", timeout=10000)
                button.click()
                page.wait_for_load_state("networkidle", timeout=10000)

            except:
                break

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        # Parse the HTML and get the victim names
        victims = soup.find_all('span', class_ = 'text-xs text-white')
        with open("./INC Ransom/INC Ransom_victims.txt", "w") as f:
            for victim in victims:
                victim_name_text = victim.text.strip()
                f.write(f"{victim_name_text}\n")
                print(victim_name_text)

        browser.close()
    # Track the end time, so the amount of time the function runs can be calculated
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./INC Ransom/INC Ransom_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")

if __name__ == "__main__":
    # The code below allows the script to be run on its own
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    dir_path = f"./{cybercriminal_org}"
    os.makedirs(dir_path, exist_ok=True)
    # If a scraping function is added, include the name in the
    # dictionary below
    scraping = {
        "scrape_rhysida": scrape_rhysida,
        "scrape_play": scrape_play,
        "scrape_inc_ransom": scrape_inc_ransom
    }
    scraping_func_name = os.getenv("SCRAPING_FUNC")
    scraping_func = scraping.get(scraping_func_name)
    scraping_func()
