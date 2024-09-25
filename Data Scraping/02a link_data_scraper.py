import requests
from bs4 import BeautifulSoup
import csv

def extract_data(url):
    # Make a request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div with class "hilightBold"
    hilight_bold_div = soup.find("div", class_="hilightBold")

    # Extract the data from the div
    if hilight_bold_div:
        return hilight_bold_div.text
    else:
        return "Div with class 'hilightBold' not found."

def remove_filler(data):
    junk_text = """See More Samples on Allergy / Immunology

Allergic Rhinitis
Allergy Evaluation Consult
Asthma in a 5-year-old
Chronic Sinusitis
Ethmoidectomy and Mastoid Antrostomy
Evaluation of Allergies
Followup on Asthma
Kawasaki Disease - Discharge Summary



Go Back to Allergy / Immunology




View this sample in Blog format on MedicalTranscriptionSamples.com"""
    return data.replace(junk_text, '').strip()


def main():
    with open('table_links.csv', 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            data = extract_data(url)
            cleaned = remove_filler(data)
            print(f"Data from {url}:{cleaned}")

if __name__ == "__main__":
    main()