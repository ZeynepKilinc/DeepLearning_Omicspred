
import requests
import pandas as pd
from bs4 import BeautifulSoup


import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_path = "complete_table.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file_path)
columns = ['gene', 'C', 'F', 'P','link','react']
empty_df = pd.DataFrame(columns=columns)

# Base URL for requests (update with your actual URL structure)
new_col, col_C, col_F, col_P,react,lin = [], [], [], [],[],[]
count=0
# Iterate over the first column
for element in data.iloc[0:, 0]:  # Reads the first column (index 0)
    # Construct the full URL (assuming the first column values are appended to the base URL)
    full_url = 'https://metabolomicsworkbench.org/databases/proteome/MGP_detail.php?MGP_ID=' + element + '&MODE=GENE'
    try:
        response = requests.get(full_url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'verticaldatatable'})   
        table2 = table.find_next_sibling('table', {'class': 'verticaldatatable'})  
    except requests.RequestException as e:
        print(f"Error requesting {full_url}: {e}")
        continue
    
    # Extract rows from the table
    rows = table.find_all("tr")[1:] 
    extracted_data_C, extracted_data_F, extracted_data_P,li,re = [], [], [],[],[]
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            type_value = cells[2].text.strip()  # First component (C, F, or P)
            description_value = cells[3].text.strip()  # Second component
            
            # Sort the descriptions into respective lists based on type_value
            if type_value == 'C':
                extracted_data_C.append(description_value)
            elif type_value == 'F':
                extracted_data_F.append(description_value)
            elif type_value == 'P':
                extracted_data_P.append(description_value)
    if table2:
        rows = table2.find_all("tr")[1:]     
        rows = table.find_all('tr') if table else []

        for row in rows:
            link_tag = row.find('a')  # Find the <a> tag
            if link_tag:
                link = link_tag['href']  # Extract link (href attribute)
                link_text = link_tag.text.strip()  # Extract text from the <a> tag
                description = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else ''  # Extract description text
                    
                    # Append values to columns
                li.append(link)  # Link
                re.append(link_text)  # Link text
    
    
    # Append the extracted data for the current gene
    new_col.append(element)
    lin.append(li)
    react.append(re)
    col_C.append(extracted_data_C)
    col_F.append(extracted_data_F)
    col_P.append(extracted_data_P)
    print(count)
    count+=1
# Create the DataFrame
empty_df["gene"] = new_col
empty_df["C"] = col_C
empty_df["F"] = col_F
empty_df["P"] = col_P
empty_df["link"] = link
empty_df["react"] = react
# Save the updated DataFrame
empty_df.to_csv("updated_data_split.csv", index=False)

print("Updated DataFrame saved to 'updated_data_split.csv'")