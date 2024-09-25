import pandas as pd
import csv 
import requests
from bs4 import BeautifulSoup

data = []

with open('table_links.txt', 'r') as file:
    links = file.readlines()

# Loop through each link
for idx, link in enumerate(links):
    link = link.strip()

    response = requests.get(link)

    soup = BeautifulSoup(response.content, 'html.parser')

    target_element = soup.select_one("body > main > div > div > div.col-lg-9.mainContent > div.hilightBold > div:nth-child(1) > div:nth-child(1)")
    header_of_transcript = target_element.text.replace("(Medical Transcription Sample Report)","")
    hilight_bold_div = soup.find('div', class_='hilightBold')

    if hilight_bold_div:
        hilight_bold_text = hilight_bold_div.text

        # Remove content between "See More Samples" and "Keywords"
        start_index = hilight_bold_text.find("See More Samples")
        end_index = hilight_bold_text.find("Keywords")
        if start_index != -1 and end_index != -1:
            hilight_bold_text = hilight_bold_text[:start_index] + hilight_bold_text[end_index:]

        # Find the start and end points of the content
        start = hilight_bold_text.find("(Medical Transcription Sample Report)") + len("(Medical Transcription Sample Report)")
        end = hilight_bold_text.find("Keywords")

        if start != -1 and end != -1:
            header_of_transcript = header_of_transcript.replace("\n\n", "\n").strip()
            transcript = hilight_bold_text[start:end].strip()
            keywords_section = hilight_bold_text[end+len("Keywords"):].strip().replace(": ","")
            print(f"\n\n========Link Number: {idx + 1}========")
            header_of_transcript_lines = header_of_transcript.split('\n')
            medical_specialty = header_of_transcript_lines[0]
            medical_specialty = medical_specialty.replace("Medical Specialty:", "")

            # Dictionary entry for data list
            entry = {
                'Medical Specialty': medical_specialty,
                'Transcript' : transcript,
                'Keywords' : keywords_section 
            }
            print(transcript)
            data.append(entry)

        else:
            print(f"Desired content not found on {link}")
    else:
        print(f"'hilightBold' div not found on {link}")

df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)