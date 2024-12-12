import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re



csv_file_path = "enzyme_table.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file_path)
columns = ['compunds','reaction','pathway','module','enzyme','gene']
empty_df = pd.DataFrame(columns=columns)
compounds, reaction,pathway,module,enzyme,genes=[],[],[],[],[],[]
table,tale2,new_col='','',[]
count=0
for idx,element in data.iloc[0:10].iterrows():  
    com,r,path,mod,en,g=[],[],[],[],[],[]
    gene=element[5]
    print(gene)
    g.append(gene)
    full_url = 'https://metabolomicsworkbench.org/databases/proteome/MGP_detail.php?MGP_ID='+gene # Replace 'param' with the actual query parameter name
    response = requests.get(full_url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    gene_id_header = soup.find('th', string=lambda text: text == "Gene ID")
    gene_id_row = gene_id_header.find_parent('tr')  
    numbers = re.findall(r'>(\d+)</a>', str(gene_id_row))
    id=int(numbers[0])
    full_url='https://www.metabolomicsworkbench.org/data/g-KEGG_DB.php?geneid='+str(id)
    response = requests.get(full_url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    kegg_id_links = soup.find_all('td')[2]
    http_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
    if len(http_links)<30:
        for i in http_links:
            full_url=i
            response = requests.get(full_url)
            response.raise_for_status() 
            soup = BeautifulSoup(response.content, 'html.parser')
            product_header = soup.find('span', class_='nowrap', string='Reaction')
            product_data = product_header.find_parent('th').find_next_sibling('td')
            if product_data:
                cel_content2 = product_data.find('div', class_='cel')
                if cel_content2:
                    for i in cel_content2.text.strip().split('\n'):
                        for t in i.split(' '):
                            if 'R' in t:
                                r.append(t)

            pathway_row = soup.find('th', string="Pathway")  # Locate the <th> with "Pathway"

            if pathway_row:
                pathway_description = pathway_row.find_next('td').find_all('td')
                matches = re.findall(r'<td>([^<]+)</td>', str(pathway_description))
                for i in matches:
                    path.append(i)
            module_header = soup.find('th', string=lambda text: text and text.strip() == "Module")
            if module_header:
                module_td = module_header.find_next('td')  
                module_links = module_td.find_all('a')  
                module_texts = [link.text.strip() for link in module_links]  
                mod.append(module_texts)
            else:
                print("Module section not found.")
            module_header = soup.find('th', string=lambda text: text and text.strip() == "Enzyme")
            if module_header:
                module_td = module_header.find_next('td')  
                module_links = module_td.find_all('a')  
                module_texts = [link.text.strip() for link in module_links]  
            else:
                print("Module section not found.")


            
            
        
        compounds.append(com)
        genes.append(g)
        reaction.append(r)
        module.append(mod)
        pathway.append(path)
        enzyme.append(en)
    print(count)
    count+=1

empty_df["compunds"] = compounds
empty_df["reaction"] = reaction
empty_df["pathway"] = pathway
empty_df["module"] = module
empty_df["enzyme"] = enzyme
empty_df["gene"] = genes

if not os.path.isfile(csv_file_path):
    empty_df.to_csv('compound_table.csv', mode='w', index=False, header=True)
else:
    empty_df.to_csv('compound_table.csv', mode='a', index=False, header=False) 
