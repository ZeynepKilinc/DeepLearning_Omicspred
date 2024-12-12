import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re



csv_file_path = "complete_table.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file_path)
columns = ['enzyme', 'substrate', 'product','reaction','class','gene']
empty_df = pd.DataFrame(columns=columns)
substrates,products,pathways,enzymes,classes,genes=[],[],[],[],[],[]
table,tale2,new_col='','',[]
count=0
for idx,element in data.iloc[6000:7000].iterrows():  
    gene=element[0]

    if '|' in element[2]:
        enz=element[2].split('|')[0]

        full_url = 'https://www.genome.jp/dbget-bin/www_bget?ec:'+enz 
        
        print(f"Requesting URL: {full_url}")
        subs,prod,r,c=[],[],'',[]
        try:
            response = requests.get(full_url)
            response.raise_for_status()  
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('strong', string="No such data was found.\n"):
                print("No data found, skipping further processing.")
            else:
                substrate_header = soup.find('span', class_='nowrap', string='Substrate')
                if substrate_header!=None:

                    substrate_data = substrate_header.find_parent('th').find_next_sibling('td')
                    if substrate_data:
                        cel_content = substrate_data.find('div', class_='cel')
                        if cel_content:
                            for i in cel_content.text.strip().split('\n'):
                                subs.append(i.rstrip(';'))
                    product_header = soup.find('span', class_='nowrap', string='Product')
                    product_data = product_header.find_parent('th').find_next_sibling('td')
                    if product_data:
                        cel_content2 = product_data.find('div', class_='cel')
                        if cel_content2:
                            for i in cel_content2.text.strip().split('\n'):
                                prod.append(i.rstrip(';'))
                    r_header = soup.find('span', class_='nowrap', string='Reaction(KEGG)')
                    r_data = r_header.find_parent('th').find_next_sibling('td')
                    if r_data:
                        cel_content3 = r_data.find('div', class_='cel')
                        if cel_content3:
                            # if cel_content3.text.strip().count('R') >1:
                            #     matches = re.findall(r'R(\d.{5})', cel_content3.text.strip())                        
                            #     r=matches
                            # else:    
                            r=cel_content3.text.strip()[0:6]
                            
                    c_header = soup.find('span', class_='nowrap', string='Class')
                    c_data = c_header.find_parent('th').find_next_sibling('td')
                    if c_data:
                        cel_content4 = c_data.find('div', class_='cel')
                        if cel_content4:
                            cel_content4=cel_content4.text.strip().split('BRITE')[0]
                            for i in cel_content4.split('\n')[:-1]:
                                c.append(i.rstrip(';'))
                    enzymes.append(enz)
                    genes.append(gene)

                    substrates.append(subs)
                    products.append(prod)
                    pathways.append(r)
                    classes.append(c)
            
        except requests.RequestException as e:
            print(f"Error requesting {full_url}: {e}")
    print(count)
    count+=1
    # rows1 = table.find_all("tr")[1:] 
    # rows2 = table.find_all("tr")[1:]
    # extracted_data1 = []
    # extracted_data2 = []
            

empty_df["enzyme"] = enzymes
empty_df["substrate"] = substrates
empty_df["product"] = products
empty_df["reaction"] = pathways
empty_df["class"] = classes
empty_df["gene"] = genes



# # Step 3: Save the updated dataframe
if not os.path.isfile(csv_file_path):
    empty_df.to_csv('enzyme_table.csv', mode='w', index=False, header=True)
else:
    empty_df.to_csv('enzyme_table.csv', mode='a', index=False, header=False) 

    # new_col.append(extracted_data1)



# # Step 3: Save the updated dataframe
#data.to_csv("updated_data.csv", index=False)
