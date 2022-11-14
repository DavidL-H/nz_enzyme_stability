'''
This script takes the Uniprot sequence similarity hit, cleans it up, and downloads the alphafold strcuture for said hit via the API
David
221016
'''
import pandas as pd
from uniprot_embl_AF_API_funcs import get_AF_pdb_from_uniprot_id

# First lets clean the ss fasta uniprot query hits
train_dat = pd.read_csv("./data/train_updated_uniprot_ss_search_final.csv")
train_dat.head

# Use regex to extract the uniprot if from the ss search hit into a new column 
# e.g. "SP:Q80WW9 DDRGK_MOUSE DDRGK domain-containing" -> "Q80WW9"
train_dat['uniprot_id'] = train_dat["fasta_ss_search_result"].str.extract('SP:(.*?)\s', expand=True)
train_dat.head

# Let extract just the unique uniprot IDs
unique_ids = train_dat['uniprot_id'].unique()


# https://www.blopig.com/blog/2022/08/retrieving-alphafold-models-from-alphafolddb/
# Downloading of alphafold stuctures


AlphaFold_status = {}
for uniprot_id in unique_ids:
    uniprot_id = str(uniprot_id)
    response = get_AF_pdb_from_uniprot_id(uniprot_id,'./data/alphafold/')
    print(uniprot_id)
    print(response)
    if str(response) == '<Response [404]>':
        AlphaFold_status[uniprot_id] = 0
    elif str(response) == '<Response [200]>':
        AlphaFold_status[uniprot_id] = 1
# All the structures that could be downloaded are downloaded, now lets add the status to the df

# Yeah, I know this shouldn't be done with a loop but I'm new to Pandas. Gimme a break.
train_dat['af_pdb_status'] = pd.NA

train_dat.loc[train_dat['uniprot_id'] == 'P61989','af_pdb_status'] = 1 



train_dat.loc[]

for key in AlphaFold_status:
    print(key)
    train_dat.loc[train_dat['uniprot_id'] == key,'af_pdb_status'] = AlphaFold_status[key]



AlphaFold_status