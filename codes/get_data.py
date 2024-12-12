import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
# URL of the webpage containing the table
url = "https://www.metabolomicsworkbench.org/databases/proteome/MGP_table.php"



session = requests.Session()

# Placeholder for all rows
all_rows = []

# Define the total number of entries and entries per page
total_entries = 7000  # Adjust based on the actual number
entries_per_page = 500  # Based on the default

# Start pagination
for start in range(0, total_entries, entries_per_page):
    print(f"Fetching records starting from entry {start + 1}...")
    
    # Update the payload based on the form fields
    payload = {
        'MGP_ID': '',               # Hidden field value
        'GENE_ID': '',              # Hidden field value
        'GENE_NAME': '',            # Hidden field value
        'TAXID': '',                # Hidden field value
        'STATUS': 'current',        # Hidden field value
        'GENE_SYMBOL': '',          # Hidden field value
        'PROTEIN_ENTRY': '',        # Hidden field value
        'PATHWAY_NAME': '',         # Hidden field value
        'SMP_PATHWAY_ID': '',       # Hidden field value
        'REACTOME_PATHWAY_ID': '',  # Hidden field value
        'sort': '',                 # Hidden field value
        'rss': start,                # Hidden field value
        'nums': entries_per_page,    # Number of entries to fetch per page
        'flag': start,              # Starting index (pagination control)
        'submit': 'Get next 500 of 7323 records'
    }
    
    # Send the POST request
    response = session.post(url, data=payload)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table
    table = soup.find('table', {'class': 'MGPdtable'})    
    if not table:
        print("No more data found.")
        break

    # Extract rows from the table
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
        rows.append(cells)

    # If no rows are returned, stop pagination
    if not rows:
        print("No more rows available.")
        break

    # Add rows to the master list
    all_rows.extend(rows)

# Extract headers from the first page (if available)
headers = [header.text.strip() for header in table.find_all('th')]

# Convert to DataFrame
df = pd.DataFrame(all_rows, columns=headers)

# Save the data to a CSV file
csv_file_path = "complete_table.csv"

# Write headers only if the file doesn't exist
if not os.path.isfile(csv_file_path):
    df.to_csv(csv_file_path, mode='w', index=False, header=True)
else:
    df.to_csv(csv_file_path, mode='a', index=False, header=False)
# Display the final DataFrame
print(df)




