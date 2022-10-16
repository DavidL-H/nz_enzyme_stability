'''
This script takes the Uniprot sequence similarity hit, cleans it up, and downloads the alphafold strcuture for said hit via the API
David
221016
'''
import pandas as pd
from uniprot_embl_AF_API_funcs import get_AF_pdb_from_uniprot_id

root = "./data/alphafold"
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
    response = get_AF_pdb_from_uniprot_id(uniprot_id,'./data/alphafold/')¨
    if response == '<Response [404]>':
        AlphaFold_status[uniprot_id] = 0
    elif response == '<Response [200]>':
        AlphaFold_status[uniprot_id] = 1

