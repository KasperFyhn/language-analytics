import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json
import argparse

# DECLARATION: CREATED WITH GOOGLE GEMINI

def scrape_wowhead_quest_list(zone_url: str):
    """
    Scrapes quest IDs and titles from the JavaScript data on a Wowhead Classic
    zone quest overview page.

    Args:
        zone_url (str): The URL of the Wowhead Classic quest overview page for a zone,
                e.g. `eastern-kingdoms/elwynn-forest`

    Returns:
        list: A list of dictionaries, where each dictionary contains the quest id and title.
              Returns an empty list if an error occurs or no quest data is found.
    """
    quests_data = []
    zone_name = zone_url.split('/')[-1].replace('-', ' ').title()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(zone_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag containing the WH.Gatherer.addData call
        script_tag = soup.find('script', string=re.compile(r'WH\.Gatherer\.addData\(3, 4, \{'))
        if script_tag:
            # Extract the JSON-like data within the script tag
            match = re.search(r'WH\.Gatherer\.addData\(3, 4, (\{.+?\})\);', script_tag.string)
            if match:
                try:
                    # Now, find the Listview data
                    listview_script_tag = soup.find('script', string=re.compile(r'new Listview\(\{template: \'quest\', id: \'quests\','))
                    if listview_script_tag:
                        match_listview = re.search(r'data:(\[.+?\])\}\);', listview_script_tag.string)
                        if match_listview:
                            data_str = match_listview.group(1)
                            try:
                                quest_list = json.loads(data_str)
                                for quest in quest_list:
                                    quest_id = str(quest.get('id'))
                                    quest_title = quest.get('name', 'N/A')
                                    quest_level = quest.get('level', 'N/A')
                                    quests_data.append({
                                        'id': quest_id,
                                        'title': quest_title,
                                        'level': quest_level,
                                        'zone': zone_name
                                    })
                            except json.JSONDecodeError as e:
                                print(f"Error decoding quest list JSON on {zone_url}: {e}")
                        else:
                            print(f"Warning: Could not find 'data:' in Listview script on {zone_url}")
                    else:
                        print(f"Warning: Could not find Listview script on {zone_url}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding WH.Gatherer.addData JSON on {zone_url}: {e}")
            else:
                print(f"Warning: Could not find JSON data in WH.Gatherer.addData on {zone_url}")
        else:
            print(f"Warning: Could not find WH.Gatherer.addData script tag on {zone_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {zone_url}: {e}")
    except Exception as e:
        print(f"An error occurred while parsing {zone_url}: {e}")
    finally:
        return quests_data


def scrape_wowhead_quest_text(quest_url: str):
    """
    Scrapes the quest description text from a Wowhead Classic quest page.

    Args:
        quest_url (str): The URL of the Wowhead Classic quest page.

    Returns:
        str: The quest description text, or "N/A" if not found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(quest_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the h2 tag with "Description"
        description_h2 = soup.find('h2', string='Description')
        # Extract all text until the next h2 tag.
        text_chunks = []
        current_element = description_h2.next_sibling
        while current_element:
            if current_element.name == 'h2':
                break  # Stop if we find another h2
            if hasattr(current_element, 'children'):
                descendant_h2 = current_element.find('h2')
                if descendant_h2:
                    break  # Stop if a descendant h2 is found
            text_chunks.append(current_element.text.strip())
            current_element = current_element.next_sibling
        quest_text = ' '.join(text_chunks).strip()

        return quest_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {quest_url}: {e}")
        return "N/A"
    except Exception as e:
        print(f"An error occurred while parsing {quest_url}: {e}")
        return "N/A"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape quest data from Wowhead Classic.")
    parser.add_argument("output_folder",
                        help="Path to the output folder.")
    parser.add_argument("zones", nargs='+',
                        help="List of zones to scrape (e.g., eastern-kingdoms/elwynn-forest eastern-kingdoms/westfall)")
    parser.add_argument("--exclude", "-x", nargs='+',
                        help="List of phrases in quest titles to exclude from scraping.")
    args = parser.parse_args()

    output_folder = args.output_folder
    zones = args.zones

    for zone_path in zones:
        all_quests = []
        url = f"https://www.wowhead.com/classic/quests/{zone_path}"
        print(f"Extracting quest list from {url}")
        quests = scrape_wowhead_quest_list(url)

        # certain special quests can be excluded by specific phrases
        if args.exclude:
            for exclude_phrase in args.exclude:
                quests = [quest for quest in quests if exclude_phrase.lower() not in quest['title'].lower()]

        if quests:
            print(f"Successfully extracted {len(quests)} quests from {zone_path}")
            for quest in quests:
                quest_url = f"https://www.wowhead.com/classic/quest={quest['id']}"
                time.sleep(random.uniform(.01, .04))  # Do not bombard the page
                quest_text = scrape_wowhead_quest_text(quest_url)
                quest['text'] = quest_text  # Add the text to the quest dictionary
                print(f"Scraped text for quest: {quest['title']}")
            all_quests.extend(quests)

        # Save the scraped data to a JSON file
        zone_name = zone_path.split('/')[-1]
        output_file = f"{output_folder}/{zone_name}.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_quests, f, ensure_ascii=False, indent=4)
            print(f"Successfully saved {len(all_quests)} quests to {output_file}")
        except Exception as e:
            print(f"Error saving data to {output_file}: {e}")
        print("-" * 30)

