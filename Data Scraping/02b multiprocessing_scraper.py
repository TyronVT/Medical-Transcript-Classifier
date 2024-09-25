import time
import pandas as pd
import csv 
import requests
from bs4 import BeautifulSoup
import concurrent.futures
# List to contain all the data.
data = []

def process_link(link):
    entry = {}
    # Remove any leading or trailing whitespace
    link = link.strip()

    # Send a request to the webpage
    response = requests.get(link)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get Medical Specialty, Sample Name, and Description
    target_element = soup.select_one("body > main > div > div > div.col-lg-9.mainContent > div.hilightBold > div:nth-child(1) > div:nth-child(1)")
    header_of_transcript = target_element.text.replace("(Medical Transcription Sample Report)","")
    # Find the parent div "hilightBold"
    hilight_bold_div = soup.find('div', class_='hilightBold')

    if hilight_bold_div:
        # Extract the entire text content within "hilightBold"
        hilight_bold_text = hilight_bold_div.text

        # Remove content between "See More Samples" and "Keywords"
        start_index = hilight_bold_text.find("See More Samples")
        end_index = hilight_bold_text.find("Keywords")
        if start_index != -1 and end_index != -1:
            hilight_bold_text = hilight_bold_text[:start_index] + hilight_bold_text[end_index:]

        # Find the start and end points of the desired content
        start = hilight_bold_text.find("(Medical Transcription Sample Report)") + len("(Medical Transcription Sample Report)")
        end = hilight_bold_text.find("Keywords")

        if start != -1 and end != -1:
            # Clean header of transcript section.
            header_of_transcript = header_of_transcript.replace("\n\n", "\n").strip()

            # Extract the desired portion
            transcript = hilight_bold_text[start:end].strip()

            # Include all words after "Keywords"
            keywords_section = hilight_bold_text[end+len("Keywords"):].strip().replace(": ","")

            header_of_transcript_lines = header_of_transcript.split('\n')
            medical_specialty = header_of_transcript_lines[0]
            medical_specialty = medical_specialty.replace("Medical Specialty:", "")

            # Dictionary entry for data list
            entry = {
                'Medical Specialty': medical_specialty,
                'Transcript' : transcript,
                'Keywords' : keywords_section 
            }
            data.append(entry)
            #print(f"Appended to list: {link}\n{entry['Medical Specialty']}")
            print(f"\n\n{link}\n\n")
            print(f"============{transcript}++++++++++++++")
        else:
            print(f"Desired content not found on {link}")
    else:
        print(f"'hilightBold' div not found on {link}")


# Read the links from the text file
with open('01-output-table_links.txt', 'r') as file:
    links = file.readlines()

threadtimestart = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_link, links)
threadtimeend = time.time()
print(f"Total time:{threadtimeend - threadtimestart}")

df = pd.DataFrame(data)
df.to_csv('02b-output-complete_data.csv', index=False)
