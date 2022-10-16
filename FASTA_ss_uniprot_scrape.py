"""
Use the FASTA sequence similarity search API to query with nz protein stability test data aa sequences.
The data will be saved as a txt file, with the protein ids given in the test data as the keys, and the output from
the ss seach as the results/values. The idea is that we want a uniprot entru associated with each of the 
sequences in the test data set, to use for gathering AlphaFold structures down the line.

David Lennox-Hvenekilde
221001
"""
import uniprot_embl_AF_API_funcs as fas
import time
import pandas as pd

# Impor the updated dataset.
train_df = pd.read_csv("./data/train_updated.csv")
train_df.head()

# Add new columns
train_df['fasta_ss_search_result'] = pd.NA

# Test
for n in range(28944, len(train_df)):
    test_seq = train_df["protein_sequence"][n]
    jobID = fas.post_fasta_ss_search(fas.aaseq_to_request_string(test_seq, "test_title"))
    # Wait til job is done, before getting results
    while not fas.status_fasta_ss_search(jobID):
        print(jobID + " still running. Waiting 2 seconds")
        time.sleep(2)
    print("Job done, getting results")
    train_df['fasta_ss_search_result'][n] = fas.get_plain_text_result(jobID)
    # Save results
    print("Sequence nr. " + str(n) + " saved...")
    train_df.to_csv("./data/train_updated_uniprot_ss_search_v9.csv")



'''
Second run of the API Fasta BLAST search using the missing values data frame,
The output of "./data/data_clean.py"
'''

# Rerun the search with the missing values dataframe
train_df_missing = pd.read_csv("./data/train_updated_uniprot_ss_search_missing.csv")
train_df_missing.head()
train_df_missing['fasta_ss_search_result'] = pd.NA

for n in range(len(train_df_missing)):
    test_seq = train_df_missing["protein_sequence"][n]
    jobID = fas.post_fasta_ss_search(fas.aaseq_to_request_string(test_seq, "test_title"))
    # Wait til job is done, before getting results
    while not fas.status_fasta_ss_search(jobID):
        print(jobID + " still running. Waiting 2 seconds")
        time.sleep(2)
    print("Job done, getting results")
    train_df_missing['fasta_ss_search_result'][n] = fas.get_plain_text_result(jobID)
    # Save results
    print("Sequence nr. " + str(n) + " saved...")
    train_df_missing.to_csv("./data/train_updated_uniprot_ss_search_v10.csv")