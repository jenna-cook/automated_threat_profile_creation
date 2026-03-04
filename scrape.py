from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import TimeoutError, Error
import time
import os
from datetime import datetime


def scrape_rhysida():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./Rhysida/Rhysida_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")

    tor_proxy = "socks5://127.0.0.1:9050"  # tor daemon, NOT torify

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )

        page = browser.new_page()
        page.goto("http://rhysidafohrhyy2aszi7bm32tnjat5xri65fopcxkdfxhi4tidsg7cad.onion/archive.php", wait_until="domcontentloaded")

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
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
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./Rhysida/Rhysida_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")

def scrape_play():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./Play/Play_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")
    
    tor_proxy = "socks5://127.0.0.1:9050"  # tor daemon, NOT torify

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )
        with open("./Play/Play_victims.txt", "w") as f:
            page_num = 1
            max_page_num = 1
            while page_num <= max_page_num:
                page = browser.new_page()
                for i in range(5):
                    try:
                        page.goto(f'http://k7kg3jqxang3wh7hnmaiokchk7qoebupfgoik6rha6mjpzwupwtj25yd.onion/index.php?page={page_num}', wait_until="domcontentloaded")
                    except (TimeoutError, Error) as e:
                        print(f"Error {e} - Sleepig for {2 ** i} seconds")
                        time.sleep(2 ** i)
                    else:
                        break
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                if page_num == max_page_num:
                    pages = soup.find_all('span', class_='Page')
                    max_page_num = int(pages[len(pages)-1].text.strip())
                    print(f"max page number: {max_page_num}")
                victims = soup.find_all('th', class_ = 'News')
                for victim in victims:
                    victim_link = victim.find('i', class_='link')
                    victim_link_text = victim_link.next_sibling.text.strip()
                    victim_name_text = victim.find(string=True, recursive=False)
                    f.write(f"{victim_name_text} ({victim_link_text})\n")
                    print(f"{victim_name_text} ({victim_link_text})\n")
                page_num += 1
        browser.close()
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./Play/Play_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")

def scrape_inc_ransom():
    start_time = datetime.now()
    formatted_time = start_time.strftime("Start time: %H:%M:%S")
    with open("./INC Ransom/INC Ransom_timestamps.txt", "a") as time_file:
        time_file.write("Scraping...\n")
        time_file.write(f"{formatted_time}\n")

    tor_proxy = "socks5://127.0.0.1:9050"  # tor daemon, NOT torify

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={"server": tor_proxy}
        )

        page = browser.new_page()
        page.goto("http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures", wait_until="networkidle")

        while True:
            try:
                button = page.wait_for_selector(".more__container.text-primary.cursor-pointer.p-12.text-sm", timeout=10000)
                button.click()
                page.wait_for_load_state("networkidle", timeout=10000)

            except:
                break

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        victims = soup.find_all('span', class_ = 'text-xs text-white')
        with open("./INC Ransom/INC Ransom_victims.txt", "w") as f:
            for victim in victims:
                victim_name_text = victim.text.strip()
                f.write(f"{victim_name_text}\n")
                print(victim_name_text)

        browser.close()
    end_time = datetime.now()
    formatted_time = end_time.strftime("End time: %H:%M:%S")
    with open("./INC Ransom/INC Ransom_timestamps.txt", "a") as time_file:
        time_file.write(f"{formatted_time}\n")

if __name__ == "__main__":
    cybercriminal_org = os.getenv("CYBERCRIMINAL_ORG")
    dir_path = f"./{cybercriminal_org}"
    os.makedirs(dir_path, exist_ok=True)
    scraping = {
        "scrape_rhysida": scrape_rhysida,
        "scrape_play": scrape_play,
        "scrape_inc_ransom": scrape_inc_ransom
    }
    scraping_func_name = os.getenv("SCRAPING_FUNC")
    scraping_func = scraping.get(scraping_func_name)
    scraping_func()
