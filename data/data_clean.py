'''
Clean up data set from the FASTA_ss_uniprot_scape.py
These are csv files with Fasta BLAST hits again the uniprot database, using the training dataset.
The hits are spread across several .csv files, and must be cleaned.
221015
David
'''
import numpy as np
import pandas as pd
import os
import re

# We did the ss BLAST search with the uniprot API, but had to run it several times due to crashing/overloading the API calling
# This mean we ended up with the data split in several .csv files, and need to gather and clean it:
# Read in the first, incomplete ss_search file, with some BLAST hits
train_dat_ss = pd.read_csv("./data/train_updated_uniprot_ss_search.csv")

# Subset to get only rows with hits
train_dat_ss = train_dat_ss[pd.notna(train_dat_ss['fasta_ss_search_result'])]

# Loop through the rest of the data files and append to the data frame:
data_files = os.listdir(os.getcwd()+"./data")
for file in data_files:
    if re.findall('ss_search_v', file) == ['ss_search_v']:
        print(file + " being added")
        train_dat_append = pd.read_csv("./data/"+file)
        train_dat_append = train_dat_append[pd.notna(train_dat_append['fasta_ss_search_result'])]
        train_dat_ss = pd.concat([train_dat_ss, train_dat_append], ignore_index = True, sort = False)


train_dat_ss.head
for col in train_dat_ss.columns:
    print(col)
train_dat_ss = train_dat_ss.drop(["Unnamed: 0",], axis = 1)
train_dat_ss = train_dat_ss.drop(["Unnamed: 0.1"], axis = 1)
train_dat_ss = train_dat_ss.drop(["Unnamed: 0.1.1"], axis = 1)

# We not have a concatenated dataframe with all the sequene search hits
# Let se if we are missing any row in our new ss dataset, compared to the original
train_dat_original = pd.read_csv("./data/train_updated.csv")
print(len(train_dat_original)) # 2891
print(len(train_dat_ss)) # 2918

# We are indeed missing a few entries in our new data. Let find out which so we can resumbit these for ss search with Fasta BLAST
train_dat_ss_ids = train_dat_ss["seq_id"].tolist() 
train_dat_original_ids = train_dat_original["seq_id"].tolist()
missing_ids = [id for id in train_dat_original_ids if id not in train_dat_ss_ids]

# Lets make a new DF with only the rows missing these values, this will be saved and resubmitted for ss search.
train_dat_original_ss_missing = train_dat_original.loc[train_dat_original["seq_id"].isin(missing_ids)]
# only if any is missing
if len(train_dat_original_ss_missing) > 0:
    train_dat_original_ss_missing.to_csv('./data/train_updated_uniprot_ss_search_missing.csv')
else:
    train_dat_ss.to_csv('./data/train_updated_uniprot_ss_search_final.csv')
