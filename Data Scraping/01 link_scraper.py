import csv
import requests
from bs4 import BeautifulSoup

# Make a request to the website
url = 'https://www.mtsamples.com/index.asp'
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags and extract the 'href' attribute
links = [a['href'] for a in soup.find_all('a') if 'href' in a.attrs]

# Filter links based on the specified pattern
desired_links = [link for link in links if "/site/pages/browse.asp?type=" in link]

i = 0
all_table_links = []
# Print the desired links
for link in desired_links:
    response = requests.get("https://www.mtsamples.com/" + link)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table',{'id' : 'tblSamples'})
    if table:
        # Fix the list comprehension indentation
        table_links = [a['href'] for a in table.find_all('a') if 'href' in a.attrs]
        print(table_links)
        all_table_links.extend(table_links)
    else:
        print("No table found.")

csv_file = 'table_links.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for link in all_table_links:
        writer.writerow([link])
        print(f"Saved Link: {link}")

print(f"Links saved in {csv_file}")
